from time import sleep
from picamera import PiCamera
import os

camera = PiCamera()
camera.resolution = (480, 480)
camera.start_preview()

#camera warm-up time
if not os.path.exists("./imagesCaptured"):
	os.makedirs("./imagesCaptured")

maxImages = 100
for imageIndex in range(maxImages):
	sleep(2)
	imageIndex +=1
	filename = "./imagesCaptured/image_" + str(imageIndex) +".jpg"
	camera.capture(filename)

'''
1. theraml (argument, should auto
2. sleep(, while , 10 pics / second
3. resolution(
'''
    
