import cv2

vidcap = cv2.VideoCapture('woo yeah baby.mp4')
success, image = vidcap.read()

count = 1
while success:
    cv2.imwrite("frames/frame%d.png" % count, image)
    success, image = vidcap.read()
    print('Read a new frame: ', success)    
    count += 1
