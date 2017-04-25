import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from face.face_module_interface import *
from GlobalEntities import *
sys.path.append(AlignDlibrary)
from align_dlib import AlignDlib
import numpy as np
import cv2

class OpenFaceEngine(FaceInterface):

    def __init__(self, engine):
        self.__engine = engine
        self.__AlignDlib__= AlignDlib(openfaceModule+'shape_predictor_68_face_landmarks.dat')

    def detect_faces(self, img):
        # cv2.namedWindow("img", cv2.WINDOW_NORMAL)
        img = cv2.imread(img)

        faces = []
        faceRects = []
        rects = []
        rects = self.__AlignDlib__.getAllFaceBoundingBoxes(img)
        for x in range(len(rects)):
            rectObject = rects[x]
            rectPoints = (rectObject.left(), rectObject.top(),
                rectObject.right(),rectObject.bottom())
            faceRects.append(rectPoints)
        for(x, y, w, h) in faceRects:
            cv2.rectangle(img,(x,y),(w,h),(0,0,255),3)
            roi_color = img[y:h, x:w]
            faces.append(roi_color)
        # cv2.imshow('img',img)
        # cv2.waitKey(0)
        return [img, faces, faces_rects]
