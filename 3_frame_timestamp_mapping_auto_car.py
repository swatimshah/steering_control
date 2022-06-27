# Import necessary libraries
import cv2
import time
import numpy
from numpy import savetxt 
import pafy

# set path in which you want to save images
csv_file = "auto_car.csv"

# Open the link
video = cv2.VideoCapture('movie.mp4')

# Extract hight, width and framerate from the video
print(video.get(cv2.CAP_PROP_FRAME_WIDTH))
print(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(video.get(cv2.CAP_PROP_FPS))

frame_id = 0;
data_list = numpy.empty([0, 2])
data = numpy.empty([2])
font = cv2.FONT_HERSHEY_PLAIN

while True:
	# Read video by read() function and it
	# will extract and return the frame

	ret, img = video.read()

	if img is None:
		break;

	# Initialize the dimentions of the video for the first time, for resizing. 
	# For future frames the same dimentions will be used. 
	if (frame_id == 0):
		scale_percent = 35 # percent of original size
		width = int(img.shape[1] * scale_percent / 100)
		height = int(img.shape[0] * scale_percent / 100)
		dim = (width, height)

	resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

	# Put current DateTime on each frame
	my_timestamp = round(time.time(), 3)
	cv2.putText(resized, str(frame_id), (20, 40),
				font, 2, (255, 255, 255), 2, cv2.LINE_AA)
	
	data[0] = frame_id
	data[1] = my_timestamp

	data_list = numpy.append(data_list, data.reshape(1, 2), axis=0)

	frame_id = frame_id + 1
	
	cv2.imshow('live video', resized)

	# wait for user to press any key
	key = cv2.waitKey(40)

# close the camera
video.release()

# close open windows
cv2.destroyAllWindows()

numpy.savetxt(csv_file, data_list, delimiter=",", header="frame_id, timestamp")