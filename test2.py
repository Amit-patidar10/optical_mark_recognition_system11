import cv2
import numpy as np
import utlis

####################################################
test_image = "./image/1.jpg"
widthImg = 700
hightImg = 600
questions = 5
choices = 5
answer  = [1,2,0,1,4]
webCamFeed = True
camera_no = 1
cap = cv2.VideoCapture(camera_no)
cap.set(10,150)

####################################################





	if webCamFeed:success, img = cap.read()
	else:img = cv2.imread(test_image) #original img
	img = cv2.resize(img,(widthImg,hightImg)) #resize original img
	imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #converting img from BGR(which is default color format in opencv) to gray(black & white)
	imgBlur = cv2.GaussianBlur(imgGray,(5,5),0) #making img smooth so it will detect imp. edge only
	imgCanny = cv2.Canny(imgBlur,10,50) #detecting edge using Canny function
	imgContour = img.copy()
	Biggest_contour_Img = img.copy()
	grade_Point_Img = img.copy()
	imgFinal = img.copy()

	## FINDING ALL OUR CONTOURS
	contours,hierarchy = cv2.findContours(imgCanny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
	cv2.drawContours(imgContour,contours,-1,(0,225,0),10)



	##FINDING RECTANGULAR CONTOURS & CORNER POINTS
	rectCon = utlis.rectContour(contours)
	Biggest_contour = utlis.getCornerPoints(rectCon[0])
	grade_Point = utlis.getCornerPoints(rectCon[1])


	if Biggest_contour.size != 0 and grade_Point.size != 0:
		cv2.drawContours(Biggest_contour_Img,Biggest_contour,-1,(0,225,0),20)
		cv2.drawContours(Biggest_contour_Img,grade_Point,-1,(225,0,0),20)

		pt1 = np.float32(Biggest_contour)
		pt2 = np.float32([[0,0],[0,hightImg],[widthImg,hightImg],[widthImg,0]])
		matrix = cv2.getPerspectiveTransform(pt1,pt2)
		img_warp_colored = cv2.warpPerspective(img,matrix,(widthImg,hightImg))

		ptG1 = np.float32(grade_Point)
		ptG2 = np.float32([[0,0],[0,150],[325,150],[325,0]])
		matrixG = cv2.getPerspectiveTransform(ptG1,ptG2)
		imgGradeDisplay = cv2.warpPerspective(img,matrixG,(325,150))
		#cv2.imshow("grade",imgGradeDisplay)



	##APPLYING THRESHOLD

	imgWarpGray = cv2.cvtColor(img_warp_colored,cv2.COLOR_BGR2GRAY)
	imgThresh = cv2.threshold(imgWarpGray,180,255,cv2.THRESH_BINARY_INV)[1]

	boxes = utlis.splitBoxes(imgThresh)
	#cv2.imshow("test",boxes[7])




	## TO FIND NON ZERO PIXEL VALUE OF EACH INDIVIDUAL MARK POINT


	MyPixelVal = np.zeros([questions,choices])
	countR = 0
	countC = 0

	for image in boxes:
		total_Pixels = cv2.countNonZero(image)
		
		MyPixelVal[countR][countC] = total_Pixels
		countC+=1
		if (countC == choices): countR+=1 ; countC = 0
	print(MyPixelVal)


	MyIndex =[]
	for x in range(0,choices) :
		arr = MyPixelVal[x]
		##print("arr",arr)
		MyIndexVal = np.where(arr == np.amax(arr))
		##print(MyIndexVal[0])
		MyIndex.append(MyIndexVal[0][0])
	print(MyIndex)	


	## GRADING
	Grading = []
	for x in range (0,questions):
		if answer[x] == MyIndex[x]:
			Grading.append(1)
		else: 
			Grading.append(0)
	#print(Grading)
	score = (sum(Grading)/questions)*100 #FINAL GRADE
	print(score)

	##DISPLAYING ANSWER

	 #OMR MARK DISPLAY
	result_img = img_warp_colored.copy()
	result_img = utlis.showAnswers(result_img,MyIndex,Grading,answer,questions,choices)
	ImgRawDrawing = np.zeros_like(img_warp_colored)
	ImgRawDrawing = utlis.showAnswers(ImgRawDrawing,MyIndex,Grading,answer,questions,choices)
	InvMatrix = cv2.getPerspectiveTransform(pt2,pt1)
	Inv_img_warp = cv2.warpPerspective(ImgRawDrawing,InvMatrix,(widthImg,hightImg))

	 #GRADE DISPLAY
	imgRawGrade = np.zeros_like(imgGradeDisplay)
	cv2.putText(imgRawGrade,str(int(score))+"%",(50,100),cv2.FONT_HERSHEY_COMPLEX,3,(0,255,0),5)
	#cv2.imshow("grade",imgRawGrade)
	InvmatrixG = cv2.getPerspectiveTransform(ptG2,ptG1)
	InvimgGradeDisplay = cv2.warpPerspective(imgRawGrade,InvmatrixG,(widthImg,hightImg))
		
	imgFinal = cv2.addWeighted(imgFinal,1,Inv_img_warp,1,0)
	imgFinal = cv2.addWeighted(imgFinal,1,InvimgGradeDisplay,1,0)












	## OUTPUT STATEMENT
	BlankImg = np.zeros_like(img)
	ImgArray = ([img,imgGray,imgBlur,imgCanny],
		[imgContour,Biggest_contour_Img,img_warp_colored,imgThresh],
		[result_img,ImgRawDrawing,Inv_img_warp,imgFinal])

except:
	BlankImg = np.zeros_like(img)	
	ImgArray = ([img,imgGray,imgBlur,imgCanny],
			[BlankImg,BlankImg,BlankImg,BlankImg],
			[BlankImg,BlankImg,BlankImg,BlankImg])

lables = [["orignal","gray","blur","canny"],
          ["contours","CornerPoints","warpPerspective","threshold"], 
          ["Result","RawDrawing","InvWarpPerspective","Final"]]
ImgStacked = utlis.stackImages(ImgArray,0.3,lables)
cv2.imshow('orignal',ImgStacked)
cv2.imshow("final img",imgFinal)
if cv2.waitKey(1) & 0xFF == ord('s'):
	cv2.imwrite("FinalResult.jpg",imgFinal)
	cv2.waitKey(3000)

