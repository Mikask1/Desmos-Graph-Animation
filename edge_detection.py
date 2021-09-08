import numpy as np
import cv2
from matplotlib import pyplot as plt
import os
lst = os.listdir("img_sq")

for n,i in enumerate(lst):
    img = cv2.imread('img_sq/'+i,0)
    edges = cv2.Canny(img, 100, 1000)

    cv2.imwrite("edge/"+i, edges)
