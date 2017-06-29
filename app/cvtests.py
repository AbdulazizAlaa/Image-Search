import sys
sys.path.insert(0, "..")

from engine.cv.vision import vision_engine

import numpy as np
import cv2


# Load an color image in grayscale
# img = cv2.imread('/home/abdulaziz/Downloads/testcases/1.jpg',1) #change this with any other image on your computer
img = cv2.imread('/home/abdulaziz/workspace/Machine Learning/graduation_project/aziz.jpg', 1) #change this with any other image on your computer
# img = cv2.imread('/home/abdulaziz/Downloads/testcases/5.jpg',1) #change this with any other image on your computer
# img = cv2.imread('/home/abdulaziz/Downloads/testcases/6.jpg',1) #change this with any other image on your computer

# f = opencv_engine.OpenCVFaceEngine("engine")
# print "number of faces in this image is: "+str(f.number_of_faces(img))
# f.crop_faces(img)

# creating engine instance
engine = vision_engine.VisionEngine({'face_detection': 'MTCNN_engine', 'face_recognition': 'facenet', 'object_detection_recognition': 'yolo'})

# example use method store faces
engine.store_face_training_data(img, [{'name': 'yomna', 'x': 424, 'h': 393, 'y': 188, 'w': 313}], "aziz.jpg")

# print(engine.processImage(img))
