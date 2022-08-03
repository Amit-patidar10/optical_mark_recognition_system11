import cv2
import numpy as np
import utlis

####################################################
test_image = "./image/3.jpg"
widthImg = 700
hightImg = 600
questions = 5
choices = 5
answer  = [1,4,0,1,3]
webCamFeed = True
cap = cv2.VideoCapture(0)
cap.set(10,150)

####################################################
cx = 1
count = 0 # initializing variable count to 0 (used for naming saved img)
try:
	webCam_Status = input("do you have a webcam type Y FOR YES, N FOR NO ")
except:
	webCam_Status = raw_input("do you have a webcam type Y FOR YES, N FOR NO ")
if webCam_Status == ('y' or 'Y'):
	webCamFeed = True
else:
	webCamFeed = False
while True:
	if webCamFeed :
		success,img = cap.read() 
	else: 
		test_image = "./image/"+str(cx)+".jpg"
		orignalimg = test_image

		img = cv2.imread(test_image) #original img
	
	## PREPROCESSING IMAGE

	img = cv2.resize(img,(widthImg,hightImg)) #resize original img
	# cv2.imshow("original image",img)
	imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #converting img from BGR(which is default color format in opencv) to gray(black & white)
	# cv2.imshow("grayscale",imgGray)
	imgBlur = cv2.GaussianBlur(imgGray,(5,5),0) #making img smooth so it will be easy to detect imp. edge only
	# cv2.imshow("imgBlur",imgBlur)
	imgCanny = cv2.Canny(imgBlur,10,50) #detecting edge using Canny function
	# cv2.imshow("image canny",imgCanny)
	imgContour = img.copy() #creating an copy of orignal image to draw countours
	Biggest_contour_Img = img.copy() 
	grade_Point_Img = img.copy() 
	imgFinal = img.copy() 
	
	try:

		## FINDING ALL OUR CONTOURS
		contours,hierarchy = cv2.findContours(imgCanny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
		cv2.drawContours(imgContour,contours,-1,(0,225,0),10)
		# cv2.imshow("image contours",imgContour)



		##FINDING RECTANGULAR CONTOURS & CORNER POINTS
		rectCon = utlis.rectContour(contours)   #list of rectangular contours
		Biggest_contour = utlis.getCornerPoints(rectCon[0])
		grade_Point = utlis.getCornerPoints(rectCon[1])



        ## TO 
		if Biggest_contour.size != 0 and grade_Point.size != 0:
			cv2.drawContours(Biggest_contour_Img,Biggest_contour,-1,(0,225,0),20)
			cv2.drawContours(Biggest_contour_Img,grade_Point,-1,(225,0,0),20)
			# cv2.imshow("CornerPoints",Biggest_contour_Img)

			pt1 = np.float32(Biggest_contour)
			pt2 = np.float32([[0,0],[0,hightImg],[widthImg,hightImg],[widthImg,0]])
			matrix = cv2.getPerspectiveTransform(pt1,pt2)
			img_warp_colored = cv2.warpPerspective(img,matrix,(widthImg,hightImg))
			# cv2.imshow("warp perspective",img_warp_colored)

			ptG1 = np.float32(grade_Point)
			ptG2 = np.float32([[0,0],[0,150],[325,150],[325,0]])
			matrixG = cv2.getPerspectiveTransform(ptG1,ptG2)
			imgGradeDisplay = cv2.warpPerspective(img,matrixG,(325,150))
			# cv2.imshow("grade",imgGradeDisplay)



		##APPLYING THRESHOLD

		imgWarpGray = cv2.cvtColor(img_warp_colored,cv2.COLOR_BGR2GRAY)
		imgThresh = cv2.threshold(imgWarpGray,190,255,cv2.THRESH_BINARY_INV)[1]
		# cv2.imshow("applyed threshold",imgThresh)
		thresh_explain = imgThresh.copy()
		utlis.drawGrid(thresh_explain)

		boxes = utlis.splitBoxes(imgThresh)
		# cv2.imshow("test",boxes[7])




		## TO FIND NON ZERO PIXEL VALUE OF EACH INDIVIDUAL MARK POINT


		MyPixelVal = np.zeros([questions,choices])
		countR = 0
		countC = 0

		for image in boxes:
			total_Pixels = cv2.countNonZero(image) #count number of non zero pixel
			
			MyPixelVal[countR][countC] = total_Pixels
			countC+=1
			if (countC == choices): countR+=1 ; countC = 0
		print("\n non zero pixel count =\n\n",MyPixelVal)
		
		what = np.zeros_like(imgGradeDisplay)
		


		MyIndex =[]
		array_Index = 0 
		for x in range(0,choices) :
			arr = MyPixelVal[x]
			print('\narray index',array_Index, end = ' = ')
			print(arr)
			MyIndexVal = np.where(arr == np.amax(arr))
			print("max non zero pixel count = ",MyIndexVal[0])
			MyIndex.append(MyIndexVal[0][0])
			print("1D array =",MyIndex)
			array_Index+=1
		print('\nmarked array =',MyIndex)
		print("answer array =",answer)
		# cv2.putText(img=what, text='Hello', org=(50, 100), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=3, color=(0, 255, 0),thickness=3)
		# cv2.imshow('answer',what)



		## GRADING
		Grading = []
		for x in range (0,questions):
			if answer[x] == MyIndex[x]:
				Grading.append(1)
			else: 
				Grading.append(0)
		print("compaired arr=",Grading)
		print("\nsum of grading array =",sum(Grading))
		print("number of questions =",questions)
		print("score = (sum of grading array/number of questions)*100")
		score = (sum(Grading)/questions)*100 #FINAL GRADE
		print("score =",score)

		##DISPLAYING ANSWER

		 #OMR MARK DISPLAY
		result_img = img_warp_colored.copy()
		explain_img = img_warp_colored.copy() #explainer
		gridIMG = img_warp_colored.copy()
		utlis.drawGrid(gridIMG)
		result_img = utlis.showAnswers(result_img,MyIndex,Grading,answer,questions,choices)
		explain_img = utlis.Explainer(explain_img,MyIndex,Grading,answer,questions,choices)
		utlis.drawGrid(result_img)
		## cv2.imshow("answer",result_img)
		## cv2.imshow("explain_img",explain_img)

		ImgRawDrawing = np.zeros_like(img_warp_colored)
		ImgRawDrawing = utlis.showAnswers(ImgRawDrawing,MyIndex,Grading,answer,questions,choices)
		## cv2.imshow("answer warp ",ImgRqawDrawing)
		rawImage = explain_img.copy()
		utlis.drawGrid(rawImage)
		## cv2.imshow("rawImage",rawImage)

		InvMatrix = cv2.getPerspectiveTransform(pt2,pt1)
		Inv_img_warp = cv2.warpPerspective(ImgRawDrawing,InvMatrix,(widthImg,hightImg))
		## cv2.imshow("inv warp Perspective",Inv_img_warp)

		 #GRADE DISPLAY
		imgRawGrade = np.zeros_like(imgGradeDisplay)
		cv2.putText(imgRawGrade,str(int(score))+"%",(50,100),cv2.FONT_HERSHEY_COMPLEX,3,(0,255,255),5)
		# cv2.imshow("grade",imgRawGrade)
		InvmatrixG = cv2.getPerspectiveTransform(ptG2,ptG1)
		InvimgGradeDisplay = cv2.warpPerspective(imgRawGrade,InvmatrixG,(widthImg,hightImg))
		# cv2.imshow("grade display",InvimgGradeDisplay)

		imgFinal = cv2.addWeighted(imgFinal,1,Inv_img_warp,1,0)
		# cv2.imshow("Result",imgFinal)
		imgFinal = cv2.addWeighted(imgFinal,1,InvimgGradeDisplay,2,0)
		# cv2.imshow("Result",imgFinal)

		BlankImg = np.zeros_like(img)
		ImgArray = ([img,imgGray,imgBlur,imgCanny],
			[imgContour,Biggest_contour_Img,img_warp_colored,imgThresh],
			[result_img,ImgRawDrawing,Inv_img_warp,imgFinal])
		finalArray = ([img,imgFinal])
		explainArray = ([img_warp_colored,thresh_explain,gridIMG],[explain_img,rawImage,result_img])
	except:
		BlankImg = np.zeros_like(img)	
		ImgArray = ([img,imgGray,imgBlur,imgCanny],
				[BlankImg,BlankImg,BlankImg,BlankImg],
				[BlankImg,BlankImg,BlankImg,BlankImg])
		finalArray =([img,BlankImg])
		explainArray = ([BlankImg,BlankImg],[BlankImg,BlankImg])


	## OUTPUT STATEMENT
	
	lables = [["orignal","gray","blur","canny"],
	          ["contours","CornerPoints","warpPerspective","threshold"], 
	          ["Result","RawDrawing","InvWarpPerspective","Final"]]
	ImgStacked = utlis.stackImages(ImgArray,0.3)
	FinalStack = utlis.stackImages(finalArray,0.79)
	explainStack = utlis.stackImages(explainArray,0.5)
	cv2.imshow('orignal',ImgStacked)
	cv2.imshow('explain',explainStack)
	cv2.imshow('final img',FinalStack)
	cv2.imshow('test_i',rawImage)


	##KEY TO USE // TRAVERSAL
	if cv2.waitKey(0) & 0xFF == ord('s'):
		cv2.imwrite("FinalResult"+str(count)+".jpg",imgFinal)
		count+=1
	elif cv2.waitKey(0) & 0xFF == ord('l') and cx <= 3:
		if cx == 3:
			cx = 1
		else:
			cx+=1
	elif cv2.waitKey(0) & 0xFF == ord('q'):
		break
		
cap.release()
cv2.destroyAllWindows()	


