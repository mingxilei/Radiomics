"""
This script is to compute radiomics features working with Pyradiomics
-----
Reading Files: images and masks are dealt with SimpleITK
               call function 'readimgmask' to read image and corresponding mask together
-----
-----
Pre-processing: to compute intra-tumor, peri-tumor features
                call 'intraROI', 'periROI' to transform original mask
                only compute the slice containing the largest slice when passing 'dim=2'
                dilation algorithm is based on SimpleITK, by setting radius and 'itkKernal'
-----
under construction
"""

import SimpleITK as sitk
import numpy as np
import cv2, os, sys, pandas, logging, radiomics
from radiomics import featureextractor


def listdir(path):
    list_name = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.splitext(file_path)[1] == '.PNG':
            list_name.append(file_path)
    list_name.sort()
    return list_name


def readimgmask(dcmpath, maskpath):
    # read DICOM series
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(dcmpath)
    reader.SetFileNames(dicom_names)
    image = reader.Execute()
    size = image.GetSize()[::-1]  # numpy use C-order

    # read mask in '.png' series
    flist = listdir(maskpath)
    maskarray = np.zeros(size)
    for i, slice in enumerate(flist):
        temp = cv2.imread(slice, 0)
        while temp.shape != size[1:]:
            temp = cv2.resize(temp, size[1:])
        maskarray[i, :, :] = cv2.threshold(temp, 254, 1, cv2.THRESH_BINARY_INV)[1]

    # convert to SampleITK object
    mask = sitk.GetImageFromArray(maskarray)
    mask.CopyInformation(image)

    # cast mask's pixel type into sitkUInt8 (default in SampleITK)
    # trouble calculating bounding box if missing this step
    mask = sitk.Cast(mask, sitk.sitkUInt8)

    return image, mask


def findlargestslice(mask):
    maskarray = sitk.GetArrayFromImage(mask)
    slicesum = np.sum(maskarray, axis=(1, 2))
    idx = np.where(slicesum == np.max(slicesum))
    idx = idx[0]
    if np.size(idx) > 1:
        ROIslicerange = np.where(slicesum > 0)
        ROIcentral = np.mean(ROIslicerange)
        distance = np.abs(idx - ROIcentral)
        largestsliceidx = int(idx[np.argmin(distance)])
    else:
        largestsliceidx = int(idx)
    return largestsliceidx, mask.TransformIndexToPhysicalPoint([0, 0, largestsliceidx])[2]


def extract2d(image, idx):
    imagesize = image.GetSize()
    extractor = sitk.ExtractImageFilter()
    extractor.SetSize([imagesize[0], imagesize[1], 0])
    extractor.SetIndex([0, 0, idx])
    return extractor.Execute(image)


def dilate3d(mask, radiusValue, KernelType):
    dilater = sitk.BinaryDilateImageFilter()
    dilater.SetKernelRadius(radiusValue)
    dilater.SetKernelType(KernelType)
    return dilater.Execute(mask)


def fillhole2d(mask2darray):
    im_find = mask2darray.copy()
    contours, hierarchy = cv2.findContours(im_find, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    out = np.zeros_like(mask2darray)
    # check existence of holes
    for i in range(len(contours)):
        # an external contour has no parent (<0)
        if hierarchy[0, i, 3] < 0:
            cv2.drawContours(image=out, contours=contours, contourIdx=i, color=1, thickness=cv2.FILLED)
    return out


def fillhole(binarymask):
    img = sitk.GetArrayFromImage(binarymask)
    numslice = img.shape[0]
    out = np.zeros_like(img)
    for i in range(numslice):
        im = img[i, :, :]
        out[i] = fillhole2d(im)
    newmask = sitk.GetImageFromArray(out)
    newmask.CopyInformation(binarymask)
    return newmask


def generateAunnulus(dilatedmask, mask):
    mfilter = sitk.MaskNegatedImageFilter()
    return mfilter.Execute(dilatedmask, mask)


def getphysicalradius(mask, pixelradius):
    return pixelradius * (mask.GetSpacing()[0])


def periROI3d(mask, radius, kernel):
    # fill the hole if applicable
    holeremoved = fillhole(mask)
    dilatedmask = dilate3d(holeremoved, radius, kernel)
    return generateAunnulus(dilatedmask, holeremoved), getphysicalradius(mask, radius)


def periROI2d(mask, radius, kernel):
    idx, physicalposition = findlargestslice(mask)
    # fill hole
    holeremoved = fillhole(mask)
    holeremoved = extract2d(holeremoved, idx)
    dilatedmask = dilate3d(holeremoved, radius, kernel)
    newmask = generateAunnulus(dilatedmask, holeremoved)
    # pyradimics requires 3D mask
    mask2darray = sitk.GetArrayFromImage(newmask)
    out = np.zeros_like(sitk.GetArrayFromImage(mask))
    out[idx, :, :] = mask2darray
    out = sitk.GetImageFromArray(out)
    out.CopyInformation(mask)
    return out, getphysicalradius(mask, radius), idx, physicalposition


def periROI(mask, dim, radius, kernel):
    if dim == 2:
        return periROI2d(mask, radius, kernel)
    if dim == 3:
        newmask, physicalradius = periROI3d(mask, radius, kernel)
        return newmask, physicalradius, None, None


def intraROI(mask, dim):
    if dim == 2:
        sliceidx, physicalposition = findlargestslice(mask)
        maskarray = sitk.GetArrayFromImage(mask)
        newmask = np.zeros_like(maskarray)
        newmask[sliceidx, :, :] = maskarray[sliceidx, :, :]
        newmask = sitk.GetImageFromArray(newmask)
        newmask.CopyInformation(mask)
        physicalradius = None
    elif dim == 3:
        newmask = mask
        sliceidx = None
        physicalposition = None
        physicalradius = None
    return newmask, physicalradius, sliceidx, physicalposition

def findxyspacing(image):
    return image.GetSpacing()[0]


def generateExtractor(spacing, sigma, quanAlgo, quanParam):
    settings = {}
    settings['resampledPixelSpacing'] = [spacing, spacing, spacing]
    settings['interpolator'] = sitk.sitkBSpline
    settings['enableCExtensions'] = True
    settings['normalize'] = True
    settings['normalizeScale'] = 1
    settings['sigma'] = sigma
    if quanAlgo == 'binWidth':
        settings['binWidth'] = quanParam
    elif quanAlgo == 'binCount':
        settings['binCount'] = quanParam
    else:
        sys.exit('quanAlgo error.')
    extractor = featureextractor.RadiomicsFeaturesExtractor(**settings)
    extractor.disableAllImageTypes()
    extractor.enableImageTypeByName('LoG')
    extractor.enableImageTypeByName('Wavelet')
    extractor.enableImageTypeByName('Square')
    extractor.enableImageTypeByName('SquareRoot')
    extractor.enableImageTypeByName('Logarithm')
    extractor.enableImageTypeByName('Exponential')
    extractor.enableAllFeatures()
    return extractor


def calculate(extractor, image, mask, roi, dim, radius, kernel):
    if roi == 'peri':
        [newmask, physicalradius, sliceidx, physicalposition] = periROI(mask, dim, radius, kernel)
    elif roi == 'intra':
        [newmask, physicalradius, sliceidx, physicalposition] = intraROI(mask,dim)
    featurevector = extractor.execute(image, newmask)
    featurevector['physicalradius'] = physicalradius
    featurevector['largestROIindex'] = sliceidx
    featurevector['physicalposition'] = physicalposition
    return featurevector


maskdir = r'C:\Users\mingx\OneDrive\project1\testdata\10245852\c+'
dcmdir = r'C:\Users\mingx\OneDrive\project1\testdata\10245852\dicom\C'

img, mask = readimgmask(dcmdir, maskdir)
writer = sitk.ImageFileWriter()
writer.SetFileName(r'C:\Users\mingx\OneDrive\Destops\original.nrrd')
writer.Execute(mask)
radius = 5
kernel = sitk.sitkBall
dim = 3
newmask, a, b, c = intraROI(mask, dim)
writer = sitk.ImageFileWriter()
writer.SetFileName(r'C:\Users\mingx\OneDrive\Destops\modefied.nrrd')
writer.Execute(newmask)

