import cv2
import numpy as np
import utlis
import os 
from os import listdir

count = 1
widthImg = 700
hightImg = 600
 
while True:
	test_image = "./image/"+str(count)+".jpg"
	orignalimg = test_image

	img = cv2.imread(orignalimg)
	img = cv2.resize(img,(widthImg,hightImg))
	cv2.imshow("img",img)
	cv2.waitKey(0)

	if cv2.waitKey(5000) & 0xFF == ord('s') and count <= 3:
		count+=1
	elif cv2.waitKey(5000) & 0xFF == ord('q'):
		break
	else:
		count = 1

# folder_dir = "./image"
# for images 
# in os.listdir(folder_dir):
# 	if(images.endswith(".jpg")):
# 		print(images)		
# 		# img = cv2.imread(images)
# 		# # img = cv2.resize(img,(widthImg,hightImg))
# 		# cv2.imshow("img",img)
# 		# cv2.waitKey(5000)