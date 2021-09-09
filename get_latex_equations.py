import potrace
from PIL import Image

def get_trace(data):
    bitmap = potrace.Bitmap(data)
    path = bitmap.trace(potrace.POTRACE_TURNPOLICY_MINORITY)
    return path

def get_latex(filename): # written by kevinjycui, modified to fit my code
    latex = []
    path = get_trace(filename)
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

img = Image.open("edge/frame100.bmp")
latex = get_latex(img)
