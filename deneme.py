import cv2
import numpy as np

img = cv2.imread("imgim.jpg",cv2.IMREAD_GRAYSCALE)
img = cv2.resize(img,(800,600))
_, threshold = cv2.threshold(img, 155, 255, cv2.THRESH_BINARY)
cv2.imshow("threshold1",threshold)
contours, _ = cv2.findContours(threshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt,True), True)
    cv2.drawContours(img, [approx], 0, (0,0,0), 2)
    x = approx.ravel()[0]
    y = approx.ravel()[1]
    if len(approx) == 4 and cv2.contourArea(cnt) >100:
        x, y, w, h= cv2.boundingRect(approx)
        aspectRatio = float(w)/h
        print(aspectRatio)
        if aspectRatio >=0.95 and aspectRatio <=1.05:
            cv2.putText(img, "Square", (x,y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0))

cv2.imshow("ilk",img)
cv2.imshow("threshold2",threshold)
cv2.waitKey(0)
cv2.destroyAllWindows()

