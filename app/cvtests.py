import sys
sys.path.insert(0, "..")

from engine.cv.vision import vision_engine

import numpy as np
import cv2


# Load an color image in grayscale
# img = cv2.imread('/home/abdulaziz/Downloads/testcases/1.jpg',1) #change this with any other image on your computer
# img = cv2.imread('/home/abdulaziz/workspace/Machine Learning/graduation_project/aziz.jpg', 1) #change this with any other image on your computer
img = cv2.imread('/home/abdulaziz/Downloads/test/obj2.jpg',1) #change this with any other image on your computer
# img = cv2.imread('/home/abdulaziz/Downloads/testcases/6.jpg',1) #change this with any other image on your computer

# # creating engine instance
# engine = vision_engine.VisionEngine({'face_detection': 'MTCNN_engine',
#                                     'face_recognition': 'facenet',
#                                     'object_detection_recognition': False,
#                                     'captions_generation_engine': False})
# example use method store faces
# engine.store_face_training_data(img, [{'name': 'aziz', 'x': 424, 'h': 393, 'y': 188, 'w': 313}], "aziz.jpg")
# is used after Successfully tagging image by user so it can be used for training

# engine.test()


# creating engine instance
engine = vision_engine.VisionEngine({'face_detection': 'MTCNN_engine',
                                    'face_recognition': 'facenet',
                                    'object_detection_recognition': 'inception',
                                    'captions_generation_engine': True})
# example use method processImage
# process Image and returns face rectangles and face predictions and object predictions
print(engine.processImage(img))
