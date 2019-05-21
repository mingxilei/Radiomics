"""
Resample Image and mask with given pixelSpacing (x,y,z)
-----
Parameters:
    resampledPixelSpacing <- (x,y,z)
    interpolator <- simpleITK object with default BSpline
-----
Notes:
    pass 0 to keep original spacing, e.g. (0, 0.5, 0.5) == (originalXspacing, 0.5, 0.5)
Modifed from package `Pyradiomics`
"""

import numpy
import SimpleITK as sitk



def getBoundingBox(imageNode, maskNode, **kwargs):
    label = kwargs.get('label', 1)
    # Determine bounds of volume in terms of original Index coordinate space
    lssif = sitk.LabelShapeStatisticsImageFilter()
    lssif.Execute(maskNode)

    if label not in lssif.GetLabels():
        raise ValueError('Label (%d) not present in mask', label)

    # LBound and size of the bounding box, as (L_X, L_Y, [L_Z], S_X, S_Y, [S_Z])
    bb = numpy.array(lssif.GetBoundingBox(label))
    Nd = maskNode.GetDimension()

    # Determine if the ROI is within the physical space of the image
    ROIBounds = (maskNode.TransformContinuousIndexToPhysicalPoint(bb[:Nd] - .5),  # Origin
                 maskNode.TransformContinuousIndexToPhysicalPoint(bb[:Nd] + bb[Nd:] - 0.5))  # UBound
    ROIBounds = (imageNode.TransformPhysicalPointToContinuousIndex(ROIBounds[0]),  # Origin
                 imageNode.TransformPhysicalPointToContinuousIndex(ROIBounds[1]))

    # Check if any of the ROI bounds are outside the image indices (i.e. -0.5 < ROI < Im.Size -0.5)
    # The additional 0.5 is to allow for different spacings (defines the edges, not the centers of the edge-voxels
    tolerance = 1e-3  # Define a tolerance to correct for machine precision errors
    if numpy.any(numpy.min(ROIBounds, axis=0) < (- .5 - tolerance)) or \
       numpy.any(numpy.max(ROIBounds, axis=0) > (numpy.array(imageNode.GetSize()) - .5 + tolerance)):
        raise ValueError('Bounding box of ROI is larger than image space:\n\t'
                         'ROI bounds (x, y, z image coordinate space) %s\n\tImage Size %s' %
                         (ROIBounds, imageNode.GetSize()))
    return bb


def resampleImage(imageNode, maskNode, **kwargs):

    resampledPixelSpacing = kwargs['resampledPixelSpacing']
    interpolator = kwargs.get('interpolator', sitk.sitkBSpline)

    if imageNode is None or maskNode is None:
        raise ValueError('Requires both image and mask to resample')

    maskSpacing = numpy.array(maskNode.GetSpacing())
    imageSpacing = numpy.array(imageNode.GetSpacing())

    # If spacing for a direction is set to 0, use the original spacing (enables "only in-slice" resampling)
    resampledPixelSpacing = numpy.array(resampledPixelSpacing)
    resampledPixelSpacing = numpy.where(resampledPixelSpacing == 0, maskSpacing, resampledPixelSpacing)

    # Check if the maskNode contains a valid ROI. If ROI is valid, the bounding box needed to calculate the resampling
    # grid is returned.
    bb = getBoundingBox(imageNode, maskNode, **kwargs)

    # Do not resample in those directions where labelmap spans only one slice.
    maskSize = numpy.array(maskNode.GetSize())
    resampledPixelSpacing = numpy.where(bb[3:] != 1, resampledPixelSpacing, maskSpacing)

    # If current spacing is equal to resampledPixelSpacing, no interpolation is needed
    # Tolerance = 1e-5 + 1e-8*abs(resampledSpacing)
    if numpy.allclose(maskSpacing, resampledPixelSpacing) and numpy.allclose(imageSpacing, resampledPixelSpacing):
        return imageNode, maskNode

    # Calculate the new size. Cast to int to prevent error in sitk.
    spacingRatio = maskSpacing / resampledPixelSpacing
    newSize = numpy.ceil(maskSize * spacingRatio)
    newSize = numpy.array(newSize, dtype='int').tolist()

    newOriginIndex = numpy.array(.5 * (resampledPixelSpacing - maskSpacing) / maskSpacing)
    newOrigin = maskNode.TransformContinuousIndexToPhysicalPoint(newOriginIndex)

    imagePixelType = imageNode.GetPixelID()
    maskPixelType = maskNode.GetPixelID()

    direction = numpy.array(maskNode.GetDirection())


    try:
        if isinstance(interpolator, six.string_types):
            interpolator = getattr(sitk, interpolator)
    except Exception:
        interpolator = sitk.sitkBSpline

    rif = sitk.ResampleImageFilter()

    rif.SetOutputSpacing(resampledPixelSpacing)
    rif.SetOutputDirection(direction)
    rif.SetSize(newSize)
    rif.SetOutputOrigin(newOrigin)


    rif.SetOutputPixelType(imagePixelType)
    rif.SetInterpolator(interpolator)
    resampledImageNode = rif.Execute(imageNode)

    rif.SetOutputPixelType(maskPixelType)
    rif.SetInterpolator(sitk.sitkNearestNeighbor)
    resampledMaskNode = rif.Execute(maskNode)

    return resampledImageNode, resampledMaskNode