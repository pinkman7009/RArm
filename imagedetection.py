import cv2
import numpy as np

cap = cv2.VideoCapture(2)
while True:
    _, frame = cap.read()

    key = cv2.waitKey(1)
    if key == 27:
        break

    frame  = frame[230:470,1:610]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 5)
    sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpen = cv2.filter2D(blur, -1, sharpen_kernel)

    thresh = cv2.threshold(sharpen,100,255, cv2.THRESH_BINARY_INV)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

    cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# for contour in contours:
#     cv2.drawContours(copy, contour, -1, (0, 255, 0), 3)
# cv2.imshow('contours',copy)

    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    min_area = 1000
    max_area = 10000
    image_number = 0
    for c in cnts:
        area = cv2.contourArea(c)
        if area > min_area and area<max_area:
            x,y,w,h = cv2.boundingRect(c)
            ROI = frame[y:y+h, x:x+h]
            colours  = frame[int(y+h/2),int(x+h/2)]
            print("BRG",colours)
            
            font = cv2.FONT_HERSHEY_SIMPLEX 
  
# org 
            org = (x, y) 
  
# fontScale 
            fontScale = 1
   
# Blue color in BGR 
            color1 = (0, 255, 255) 
            color2 = (0,0,0)
  
# Line thickness of 2 px 
            thickness = 2
   
# Using cv2.putText() method 
           
   
            #if colours[0]>=20 and colours[0]<=35 and colours[1]>=210 and colours[1]<=225 and colours[2]<=255:
                 #frame = cv2.putText(frame, 'Yellow', org, font,  
                   #fontScale, color1, thickness, cv2.LINE_AA) 
            if colours[0]>=0 and colours[1]<=10 and colours[1]>=0 and colours[1]<=10 and colours[2]>=0 and colours[1]<=10:
                 frame = cv2.putText(frame, 'Black', org, font,  
                   fontScale, color2, thickness, cv2.LINE_AA) 
                   
            cv2.imwrite('ROI_{}.png'.format(image_number), ROI)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (36,255,12), 2)
            image_number += 1

    cv2.imshow('sharpen', sharpen)
    cv2.imshow('close', close)
    cv2.imshow('thresh', thresh)
    cv2.imshow('image', frame)
cv2.destroyAllWindows()
cap.release()