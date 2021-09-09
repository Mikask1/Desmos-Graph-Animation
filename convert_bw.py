import cv2
from PIL import Image


img = cv2.imread("mankitsu.jpg")
img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
edges = cv2.Canny(img_gray, 100, 300)
cv2.imshow("w", edges)
cv2.waitKey()
edged = Image.fromarray(edges)
edged.save("edged.bmp")
