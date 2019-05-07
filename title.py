import cv2
import numpy as np
from pythonRLSA import rlsa
import pytesseract
import math
import sys

size_ratio=1.5 # ratio compared to rest of the text

image = cv2.imread('in/title-test.png') # reading the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # converting to grayscale image
(thresh, im_bw) = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU) # converting to binary image

mask = np.ones(image.shape[:2], dtype="uint8") * 255 # create blank image of same dimension of the original image
contours, _ = cv2.findContours(~im_bw,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) 
heights = [cv2.boundingRect(contour)[3] for contour in contours] # collecting heights of each contour
avgheight = sum(heights)/len(heights) # average height

# finding the larger text
for c in contours:
    [x,y,w,h] = cv2.boundingRect(c)
    if h > size_ratio*avgheight:
        cv2.drawContours(mask, [c], -1, 0, -1)

x, y = mask.shape # image dimensions

value = max(math.ceil(x/100),math.ceil(y/100))+20
mask = rlsa.rlsa(mask, True, False, value) # rlsa application

contours, _ = cv2.findContours(~mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

mask2 = np.ones(image.shape, dtype="uint8") * 255 # blank 3 layer image
for contour in contours:
    [x, y, w, h] = cv2.boundingRect(contour)
    if w > 0.60*image.shape[1]:# width heuristic applied
        title = image[y: y+h, x: x+w] 
        mask2[y: y+h, x: x+w] = title # copied title contour onto the blank image
        image[y: y+h, x: x+w] = 255 # nullified the title contour on original image

if len(sys.argv) == 2:
    pytesseract.pytesseract.tesseract_cmd = sys.argv[1]
else:
    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract' # replace this with your tesseract location if no param
text = pytesseract.image_to_string(mask2, lang = 'eng')
print(text)

cv2.imwrite('out/title-test.png', mask2)