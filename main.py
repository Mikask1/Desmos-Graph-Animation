import cv2
from PIL import Image, ImageOps
import potrace
import numpy as np

def get_trace(data):
    bitmap = potrace.Bitmap(data)
    path = bitmap.trace(turnpolicy = potrace.POTRACE_TURNPOLICY_MINORITY, alphamax= 1.0, opticurve = True, opttolerance = 0.5)
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

def thresh(gray):
    thresh = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY)[1]
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
    img = cv2.resize(img,dim)
    cv2.imshow("", img)
    cv2.waitKey()
    
def get_edge(img): 
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    edges = otsu(img_gray, filtered=True)

    edge_pil = Image.fromarray(edges)
    return edge_pil

def inputFile():
    import tkinter.filedialog as fd
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    input_file = fd.askopenfilenames(parent=root, title='Choose image to graph')
    return input_file

img = Image.open(inputFile()[0])
img = ImageOps.flip(img)

latex = get_latex(np.asarray(img))

with open("latex.txt", "w") as file:
    file.writelines("%s\n" % l for l in latex)
