import cv2
from PIL import Image, ImageOps
import potrace
import numpy as np

def get_trace(data):
    bitmap = potrace.Bitmap(data)
    path = bitmap.trace(turnpolicy = potrace.POTRACE_TURNPOLICY_MINORITY, alphamax= 1.0, opticurve = True, opttolerance = 0.8)
    return path

def get_latex(img): # written by kevinjycui, modified to fit my code
    latex = []
    path = get_trace(get_edge(img))
    for curve in path.curves:
        segments = curve.segments
        start = curve.start_point
        for segment in segments:
            x0 = start.x
            y0 = start.y
            if segment.is_corner:
                x1 = segment.c.x
                y1 = segment.c.y
                x2 = segment.end_point.x
                y2 = segment.end_point.y
                latex.append('((1-t)%f+t%f,(1-t)%f+t%f)' % (x0, x1, y0, y1))
                latex.append('((1-t)%f+t%f,(1-t)%f+t%f)' % (x1, x2, y1, y2))
            else:
                x1 = segment.c1.x
                y1 = segment.c1.y
                x2 = segment.c2.x
                y2 = segment.c2.y
                x3 = segment.end_point.x
                y3 = segment.end_point.y
                latex.append('((1-t)((1-t)((1-t)%f+t%f)+t((1-t)%f+t%f))+t((1-t)((1-t)%f+t%f)+t((1-t)%f+t%f)),\
                (1-t)((1-t)((1-t)%f+t%f)+t((1-t)%f+t%f))+t((1-t)((1-t)%f+t%f)+t((1-t)%f+t%f)))' % \
                (x0, x1, x1, x2, x1, x2, x2, x3, y0, y1, y1, y2, y1, y2, y2, y3))
            start = segment.end_point
    return latex

def get_edge(img, sigma = 0.33): 
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Get threshold using Otsu's method
    upper, thresh_im = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    lower = sigma*upper

    edges = cv2.Canny(img_gray, lower, upper)
    edge_pil = Image.fromarray(edges)
    return edge_pil

img = Image.open("chika.png")
img = ImageOps.flip(img)

latex = get_latex(np.asarray(img))

with open("latex.txt", "w") as file:
    file.writelines("%s\n" % l for l in latex)