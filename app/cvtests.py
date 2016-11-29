import sys
sys.path.insert(0, "..")
from engine.cv.face import face
import numpy as np
import cv2

# Load an color image in grayscale
img = cv2.imread('/home/abdulaziz/Downloads/aziz.jpeg',0) #change this with any other image on your computer
face.detect_faces(img)
