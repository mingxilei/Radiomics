"""
Read '.dcm' series with corresponding mask image by SimpleITK I/O
-----
Parameters:
    dcmpath : directory of folder containing DICOM image
    maskpath : directory of folder containing corresponding mask image
-----
Notes:
    mask images are in the format of '.png', necessarily named according to corresponding DICOM slice
    e.g. 'Slice0001.png', 'Slice0002.png' correspond to '01.dcm', '02.dcm', respectively
    mask images in this sample script was marked in red and background is in white, so additional threshold is covered
"""
import SimpleITK as sitk
import numpy as np
import cv2, os


# list all mask images in order
def listdir(path,dcmseq):
    list_name = []
    numdigit = max([len(i) for i in dcmseq])
    for o in dcmseq:
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            root, ext = os.path.splitext(file_path)
            order = root[-numdigit:]
            if ext == '.PNG':
                if order == o.zfill(numdigit):
                    list_name.append(file_path)

    return list_name


def readimgmask(dcmpath, maskpath):
    # read DICOM series
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(dcmpath)
    reader.SetFileNames(dicom_names)
    image = reader.Execute()
    size = image.GetSize()[::-1]  # numpy use C-order

    # read mask in '.png' series
    dcmlist = reader.GetFileNames()
    dcmnames = list()
    for i in range(len(dcmlist)):
        dcmnames.append(os.path.splitext(os.path.basename(dcmlist[i]))[0])
    flist = listdir(maskpath, dcmnames)
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