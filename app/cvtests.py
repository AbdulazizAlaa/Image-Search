import sys
sys.path.insert(0, "..")
from engine.cv.vision import vision_engine
import numpy as np
import cv2

# Load an color image in grayscale
# img = cv2.imread('/home/abdulaziz/Downloads/testcases/1.jpg',1) #change this with any other image on your computer
img = cv2.imread('/home/abdulaziz/Downloads/testcases/3.jpg',1) #change this with any other image on your computer
# img = cv2.imread('/home/abdulaziz/Downloads/testcases/5.jpg',1) #change this with any other image on your computer
# img = cv2.imread('/home/abdulaziz/Downloads/testcases/6.jpg',1) #change this with any other image on your computer
# f = opencv_engine.OpenCVFaceEngine("engine")
# print "number of faces in this image is: "+str(f.number_of_faces(img))
# f.crop_faces(img)

f = vision_engine.VisionEngine({'face_detection': 'opencv_engine', 'face_recognition': 'facenet', 'object_detection_recognition': 'yolo'})

print(f.processImage(img))
