import cv2
import numpy as np

img = cv2.imread('in/square-test.png')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (8,8))
gray = cv2.dilate(gray, kernel, iterations=1)

ret,gray = cv2.threshold(gray, 254, 255, cv2.THRESH_TOZERO)
ret,gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV)

gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)

contours, hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

def biggestRectangles(contours):
    indexReturn = -1
    for index in range(len(contours)):
            i = contours[index]
            area = cv2.contourArea(i)
            if area > 500:
                peri = cv2.arcLength(i,True)
                approx = cv2.approxPolyDP(i,0.1*peri,True)
                if len(approx)==4:
                        hull = cv2.convexHull(contours[index])
                        cv2.imwrite('out/square-test.png',cv2.drawContours(img, [hull], 0, (0,255,0),3))

biggestRectangles(contours)