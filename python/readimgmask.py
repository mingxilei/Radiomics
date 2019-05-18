"""
Read '.dcm' series with corresponding mask image by SimpleITK I/O
-----
Parameters:
    dcmpath : directory of folder containing DICOM image
    maskpath : directory of folder containing corresponding mask image
-----
Notes:
    mask images are in the format of '.png', necessarily named in the order of slide location.
    e.g. 'Slice1.png', 'Slice2.png', ...
"""
import SimpleITK as sitk
import numpy as np
import cv2, os


# list all mask images in order
def listdir(path):
    list_name = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.splitext(file_path)[1] == '.PNG':
            list_name.append(file_path)
    # sort by file names
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
        temp = cv2.imread(slice, cv2.IMREAD_GRAYSCALE)
        # resize mask image if size is not identical
        while temp.shape != size[1:]:
            temp = cv2.resize(temp, size[1:])
        # mark ROI as value '1' and background as '0'
        maskarray[i, :, :] = cv2.threshold(temp, 254, 1, cv2.THRESH_BINARY_INV)[1]

    # convert to SampleITK object
    mask = sitk.GetImageFromArray(maskarray)
    mask.CopyInformation(image)

    # cast mask's pixel type into sitkUInt8 (default in SampleITK)
    # trouble calculating bounding box if missing this step
    mask = sitk.Cast(mask, sitk.sitkUInt8)

    return image, mask