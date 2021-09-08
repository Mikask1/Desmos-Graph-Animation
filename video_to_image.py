import cv2
from PIL import Image

vidcap = cv2.VideoCapture('bad_apple.mp4')
success, image = vidcap.read()

count = 0
while success:
    cv2.imwrite("img_sequence/png_frame%d.jpg" % count, image)     # save frame as JPEG file      
    success, image = vidcap.read()
    print('Read a new frame: ', success)
    img = Image.open("img_sequence/png_frame%d.jpg" % count)
    img.save("img_sq/frame%d.bmp" % count)
    count += 1
