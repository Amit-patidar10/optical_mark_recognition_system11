import cv2
import numpy as np

# define a video capture object
vid = cv2.VideoCapture(0)
while(vid.isOpened()):	
	
	while(True):
		ret ,frame = vid.read()
		cv2.imshow('frame', frame)
		cv2.waitKey(1)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	vid.release()
	cv2.destroyAllWindows()
else :
	print('no camera can be found')
















# while(True):
	
# 	# Capture the video frame
# 	# by frame
# 	ret, frame = vid.read()

# 	# Display the resulting frame
# 	cv2.imshow('frame', frame)
	
# 	# the 'q' button is set as the
# 	# quitting button you may use any
# 	# desired button of your choice
# 	if cv2.waitKey(1) & 0xFF == ord('q'):
# 		break

# # After the loop release the cap object
# vid.release()
# # Destroy all the windows
# cv2.destroyAllWindows()





# image = "./image/1.jpg"
# img = cv2.imread(image)
# img = cv2.resize(img,(700,600))
# cv2.imshow('test',img)
# cv2.waitKey(0)