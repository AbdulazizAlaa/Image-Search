import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from GlobalEntities import *
from face import MTCNN_engine, opencv_engine
import numpy as np
import cv2


class VisionEngine():

    '''
    config defines the configuration for the different vision engines
    it has three keys:
    1- face_detection ====> opencv_engine/openface_engine/MTCNN_engine
    2- face_recognition ===> facenet
    3- object_detection_recognition ===> yolo
    '''
    def __init__(self, config):
        self.__config = config
        #face detection engine
        if(config['face_detection'] == 'opencv_engine'):
            self.__faceDetectionEngine = opencv_engine.OpenCVFaceEngine("engine")
        elif(config['face_detection'] == 'openface_engine'):
            self.__faceDetectionEngine = None
        elif(config['face_detection'] == 'MTCNN_engine'):
            self.__faceDetectionEngine = MTCNN_engine.MTCNNFaceEngine("")

        #face recogition engine
        if(config['face_recognition'] == 'facenet'):
            self.__faceRecognitionEngine = None

        #object detection and recognition engine
        if(config['object_detection_recognition'] == 'yolo'):
            self.__objectEngine = None


        print("Engine Created:")
        print("Face Detection Engine: ")
        print(self.__faceDetectionEngine)
        print("Face Recognition Engine: ")
        print(self.__faceRecognitionEngine)
        print("Object Engine: ")
        print(self.__objectEngine)

    def processImage(self, img):


        data = {'faces': [
                            {'name': 'aziz', 'x': 1, 'y': 1, 'w': 20, 'h': 30},
                            {'name': 'omar', 'x': 1, 'y': 1, 'w': 20, 'h': 30},
                            {'name': 'none', 'x': 1, 'y': 1, 'w': 20, 'h': 30},
                        ],'objects': [
                            {'name': 'car', 'x': 1, 'y': 1, 'w': 20, 'h': 30},
                            {'name': 'motorcycle', 'x': 1, 'y': 1, 'w': 20, 'h': 30},
                        ]
                }
        return data
