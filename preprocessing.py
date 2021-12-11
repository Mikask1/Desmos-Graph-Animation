import cv2
import numpy as np
import re

def thresh(gray, lower= 80):
    thresh = cv2.threshold(gray, lower, 255, cv2.THRESH_BINARY)[1]
    return thresh

def otsu(gray, sigma=0.33, filtered=False):
    # Get threshold using Otsu's method. Idk, I'm not a nerd
    upper, thresh_im = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    lower = sigma*upper
    if filtered:
        gray = cv2.bilateralFilter(gray, 5, 50, 50)
    edges = cv2.Canny(gray, lower, upper, L2gradient=True)
    return edges

def sigma_balls(gray, sigma = 0.33, filtered=False):
    # Get threshold with sigma thingy. Idk, I'm not a nerd.
    v = np.median(gray)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))

    if filtered:
        gray = cv2.bilateralFilter(gray, 5, 50, 50)

    edges = cv2.Canny(gray, lower, upper, L2gradient=True)
    return edges

def show_im(img, x = 50, y = 50): # shows the img in a resized form
    width = int(img.shape[1] * x / 100)
    height = int(img.shape[0] * y / 100)
    dim = (width, height)
    img = cv2.resize(img, dim)
    cv2.imshow("", img)
    cv2.waitKey()

def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)