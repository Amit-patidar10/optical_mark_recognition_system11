import cv2
import numpy as np


## TO DISPLAY NUMBER OF IMG IN SINGLE WINDOW 

def stackImages(imgArray,scale,lables=[]):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
            hor_con[x] = np.concatenate(imgArray[x])
        ver = np.vstack(hor)
        ver_con = np.concatenate(hor)
    else:
        for x in range(0, rows):
            imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        hor_con= np.concatenate(imgArray)
        ver = hor
    if len(lables) != 0:
        eachImgWidth= int(ver.shape[1] / cols)
        eachImgHeight = int(ver.shape[0] / rows)
        #print(eachImgHeight)
        for d in range(0, rows):
            for c in range (0,cols):
                cv2.rectangle(ver,(c*eachImgWidth,eachImgHeight*d),(c*eachImgWidth+len(lables[d][c])*13+27,30+eachImgHeight*d),(255,255,255),cv2.FILLED)
                cv2.putText(ver,lables[d][c],(eachImgWidth*c+10,eachImgHeight*d+20),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,0,255),2)
    return ver




## TO GET RECTENGULAR CONTOURS   

def rectContour(contours):
    rectCon = []
    for i in contours:
        Area = cv2.contourArea(i)
        ##print(Area)
        if Area > 50:
            perimeter = cv2.arcLength(i,True)
            ##print(perimeter)
            epsilon = 0.02*perimeter #MAX DIST. FROM ORIGINAL CONTOURS TO APPROX CONTOURS
            approx = cv2.approxPolyDP(i,epsilon,True)
            ##print(len(approx))
            if len(approx) == 4:
                rectCon.append(i)
    rectCon = sorted(rectCon,key = cv2.contourArea,reverse=True)
    ##print(len(rectCon))
    return rectCon



## TO GET CORNER POINT OF RECTANGULE

def getCornerPoints(cont):
        peri = cv2.arcLength(cont, True) # LENGTH OF CONTOUR
        approx = cv2.approxPolyDP(cont, 0.02 * peri, True) # APPROXIMATE THE POLY TO GET CORNER POINTS
        return approx




## TO SPLIT ALL MARK POINT INDIVIDUALLY 

def splitBoxes(img):
    rows = np.vsplit(img,5)
    # cv2.imshow("test",rows[1])
    boxes = []
    for x in rows:
        cols = np.hsplit(x,5)
        for box in cols:
         boxes.append(box)
    return boxes





def showAnswers(img,MyIndex,Grading,answer,questions,choices):
    secW = int(img.shape[1]/questions)
    secH = int(img.shape[0]/questions)

    for x in range(0,questions):
        myAns = MyIndex[x]
        cX = (myAns*secW)+secW//2
        cY = (x*secH) + secH//2

        if Grading[x] == 1:
            Mycolor = (0,255,0)
        else: 
            Mycolor = (0,0,255)
            correctAns = answer[x]
            cv2.circle(img,((correctAns*secW)+secW//2,(x*secH)+secH//2),30,(0,255,0),cv2.FILLED)


        cv2.circle(img,(cX,cY),50,Mycolor,cv2.FILLED)
    return img













