"""
fill holes of a mask image (SimpleITK object)
operated slice by slice by opencv
"""
import SimpleITK as sitk
import numpy as np
import cv2


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