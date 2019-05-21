"""
Highlight or contour the ROI of an image
-----
Call `scaleToRGB` first to scale MRI scalar data to RGB data
-----
Parameters:
    image: 3D or 4D RGB image array
    mask: mask array
------
"""
import numpy as np
import cv2
import matplotlib.cm as cm


def addContour(image,mask,c):
    if c == 'r':
        cr = (255, 0, 0)
    elif c == 'b':
        cr = (0, 0, 255)
    elif c == 'g':
        cr = (0, 255, 0)
    out = np.zeros(image.shape, dtype=mask.dtype)
    numslide = image.shape[0]
    for i in range(numslide):
        msk = mask[i].copy()
        img = image[i].copy()
        contours, hierarchy = cv2.findContours(msk, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(image=img, contours=contours, contourIdx=-1, color=cr, thickness=1)
        out[i] = img
    return out


def highlight(image,mask,c):
    if c == 'r':
        cr = (255, 0, 0)
    elif c == 'b':
        cr = (0, 0, 255)
    elif c == 'g':
        cr = (0, 255, 0)
    out = np.zeros(image.shape, dtype=mask.dtype)
    numslide = image.shape[0]
    for i in range(numslide):
        msk = mask[i].copy()
        img = image[i].copy()
        contours, hierarchy = cv2.findContours(msk, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(image=img, contours=contours, contourIdx=-1, color=cr, thickness=1)
        b, g, r = cv2.split(img)
        if c == 'r':
            b = cv2.add(b, 30, dst=b, mask=msk)
        elif c == 'g':
            g = cv2.add(g, 30, dst=g, mask=msk)
        elif c == 'b':
            r = cv2.add(r, 30, dst=r, mask=msk)
        img = cv2.merge((b, g, r))
        out[i] = img
    return out


def scaleToRGB(image):
    out = np.zeros(image.shape + (3,), dtype=np.uint8)
    numslide = image.shape[0]
    for i in range(numslide):
        scalar = cm.ScalarMappable(cmap='gray')
        out[i] = scalar.to_rgba(image[i], bytes=True)[:, :, :3]
    return out