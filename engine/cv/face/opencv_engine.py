import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from face_module_interface import *
from GlobalEntities import *
import numpy as np
import cv2

class OpenCVFaceEngine(FaceInterface):

    def __init__(self, engine):
        self.__engine = engine
        self.__face_cascade = cv2.CascadeClassifier(CascadeClassifiersFolder+'haarcascade_frontalface_default.xml')

    def detect_faces(self, img):
        """ returns array of face Rects. each rect represents a face. """
        cv2.namedWindow("img", cv2.WINDOW_NORMAL)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = []
        faces_rects = self.__face_cascade.detectMultiScale(gray, 1.3, 5)
        for(x, y, w, h) in faces_rects:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            faces.append(roi_color)
        cv2.imshow('img',img)
        cv2.waitKey(0)
        return faces
