
import numpy as np
import argparse
import imutils
import cv2

# These are the packages that we will be importing for out program
# -Numpy is a fundamental package for computing with python
# -argparse is a package used to set up a Parser.
#	What is a Parser?
# A parser is basically an analyzer for code (It breaks down your code for easier understanding)
# -Imutils is a set of functions used for basic image processing
# -OpenCV is our main image processing library
#	- This contains all the stuff related to processing and interpreting your webcam data

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

# This is where will parse the arguments (Parsing is explained above)

greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

# This is where you are defining the parameters for the color we are detecting( in this case it is green)
pts = deque(maxlen=args["buffer"])
 

if not args.get("video", False):
	camera = cv2.VideoCapture(0)

 # Read the webcam
	camera = cv2.VideoCapture(args["video"])

# If there is no webcam feed then read a video

while True:
# Grab the current frame
	(grabbed, frame) = camera.read()
 
	if args.get("video") and not grabbed:
		break
 
	frame = imutils.resize(frame, width=600)
# This is where we declare the size of the frame
	# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
# Then we blur the feed
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
# Use the BGR color set

# Create a mask for the color green
	mask = cv2.inRange(hsv, greenLower, greenUpper)
# Make the picture smoother
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

# Find shapes that are visible  under this mask(These will be only green shapes as we are running a mask which blocks out anything that is not green)
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
# If we find a shape then -->
	if len(cnts) > 0:
#		Find the largest shape and then draw a circle around it and find the center
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
#	If the shape’s radius is bigger than this size then 
		if radius > 10:
#			Draw the circle around our shape and draw the circle
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
 
# update the points queue (This is updating our list of centers as the picture could be moving)
	pts.appendleft(center)

	cv2.imshow("Frame", mask)
	key = cv2.waitKey(1) & 0xFF
# This is where we create a screen which will show what we want
 

	if key == ord("q"):
		Break
# If we hit q on the keyboard
 
camera.release()
cv2.destroyAllWindows()
# Then we will destroy the screen and break the loop

