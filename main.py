import cv2
from PIL import Image, ImageOps
import potrace
import numpy as np

def get_trace(data):
    bitmap = potrace.Bitmap(data)
    path = bitmap.trace(turnpolicy = potrace.POTRACE_TURNPOLICY_MINORITY, alphamax= 1.0, opticurve = True, opttolerance = 0.8)
    return path

def get_edge(img, sigma = 0.33): 
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Get threshold using Otsu's method | For high accuracy
    upper, thresh_im = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    lower = 0.5*upper
    filtered = cv2.bilateralFilter(img_gray, 5, 50, 50)
    edges = cv2.Canny(filtered, lower, upper, L2gradient=True)

    '''
    # Get threshold using Data Science method (idk) | For low accuracy, 1.5 times less equations
    median = max(10, min(245, np.median(img_gray)))
    lower = int(max(0, (1 - sigma) * median))
    upper = int(min(255, (1 + sigma) * median))
    edges = cv2.Canny(img_gray, lower, upper, L2gradient=True)
    '''
    
    edge_pil = Image.fromarray(edges)
    return edge_pil

def get_latex_desmos_expression(img): # written by kevinjycui, modified to fit my code
    expression = []
    path = get_trace(get_edge(img))
    n = 1
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
                n += 1
                expression.append({'id': 'graph'+str(n), 'latex': '((1-t)%f+t%f,(1-t)%f+t%f)' % (x0, x1, y0, y1), 'color': '#2b2b2b', 'lineWidth': 1.0})
                n += 1
                expression.append({'id': 'graph'+str(n), 'latex': '((1-t)%f+t%f,(1-t)%f+t%f)' % (x1, x2, y1, y2), 'color': '#2b2b2b', 'lineWidth': 1.0})
            else:
                x1 = segment.c1.x
                y1 = segment.c1.y
                x2 = segment.c2.x
                y2 = segment.c2.y
                x3 = segment.end_point.x
                y3 = segment.end_point.y
                n += 1
                expression.append({'id': 'graph'+str(n), 'latex': '((1-t)((1-t)((1-t)%f+t%f)+t((1-t)%f+t%f))+t((1-t)((1-t)%f+t%f)+t((1-t)%f+t%f)),\
                (1-t)((1-t)((1-t)%f+t%f)+t((1-t)%f+t%f))+t((1-t)((1-t)%f+t%f)+t((1-t)%f+t%f)))' % (x0, x1, x1, x2, x1, x2, x2, x3, y0, y1, y1, y2, y1, y2, y2, y3), 'color': '#2b2b2b', 'lineWidth': 1.0})
            start = segment.end_point
    return expression

def input_to_file(expression):
    with open("latex.txt", "w") as file:
        file.writelines("%s\n" % l for l in expression)
    
img = Image.open("chika.png")
img = ImageOps.flip(img)

expression = get_latex_desmos_expression(np.asarray(img))
for i in expression:
    print(i)