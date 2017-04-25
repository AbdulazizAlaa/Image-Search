import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from face.face_module_interface import *
from GlobalEntities import *
import numpy as np
import cv2

class MTCNNFaceEngine(FaceInterface):

    def __init__(self, engine):
        self.__engine = engine

    def detect_faces(self, img):
        """ returns array of face Rects and array of face mats. each entry represents a face. """
