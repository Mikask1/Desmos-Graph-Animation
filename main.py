import os
import sys
from multiprocessing import Pool

import cv2
from PIL import Image, ImageOps
import potrace
import numpy as np
import json

import preprocessing as pp

# PREPROCESSOR (Pick one)
OTSU = True
SIGMA_BALLS = False

# FILTERS (To decrease the number of equations)
FILTERED = True
L2 = False

def inputFile():
    import tkinter.filedialog as fd
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    input_file = fd.askopenfilename(parent=root, title="Choose video to graph")
    return input_file

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
                latex.append("((1-t)%f+t%f,(1-t)%f+t%f)" % (x0, x1, y0, y1))
                latex.append("((1-t)%f+t%f,(1-t)%f+t%f)" % (x1, x2, y1, y2))
            else:
                x1 = segment.c1.x
                y1 = segment.c1.y
                x2 = segment.c2.x
                y2 = segment.c2.y
                x3 = segment.end_point.x
                y3 = segment.end_point.y
                latex.append("((1-t)((1-t)((1-t)%f+t%f)+t((1-t)%f+t%f))+t((1-t)((1-t)%f+t%f)+t((1-t)%f+t%f)),\
                (1-t)((1-t)((1-t)%f+t%f)+t((1-t)%f+t%f))+t((1-t)((1-t)%f+t%f)+t((1-t)%f+t%f)))" % \
                (x0, x1, x1, x2, x1, x2, x2, x3, y0, y1, y1, y2, y1, y2, y2, y3))
            start = segment.end_point
    return latex
    
def get_edge(img): 
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    if OTSU and not SIGMA_BALLS:
        edges = pp.otsu(img_gray, L2=L2, filtered=FILTERED)
    elif SIGMA_BALLS and not OTSU:
        edges = pp.sigma_balls(img_gray, L2=L2, filtered=FILTERED)
    else:
        print("ERROR : Pick one of the preprocessors")
        sys.exit()

    edge_pil = Image.fromarray(edges)
    return edge_pil

def get_graphs(latex):
    graph_id = 0
    graphs = []
    for i in latex:
        graph_id += 1
        graphs.append({"id": "graph" + str(graph_id), "latex": i, "color": "#000000"})
    return graphs

def write_to_file(image, index):
    img = Image.fromarray(image)
    img = ImageOps.flip(img)

    graphs = get_graphs(get_latex(np.asarray(img)))
    with open("graphs/latex"+str(index)+".txt", "w") as file:
        print("Processing: frame"+str(index))
        length = len(graphs)
        for i in range(length-1):
            file.writelines(json.dumps(graphs[i])+"\n")
        file.writelines(json.dumps(graphs[i]))

if not os.path.exists("graphs"):
    os.mkdir("graphs")
    images = []
    vidcap = cv2.VideoCapture(inputFile())
    success, image = vidcap.read()
    while success:
        images += [image]
        success, image = vidcap.read()
    
    images_zip = zip(images, range(1, len(images)+1))
    pool = Pool(os.cpu_count())
    pool.starmap(write_to_file, images_zip)
    
    
    
