import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GlobalEntities import *
# from face.detection import MTCNN_engine, opencv_engine
from face.detection.MTCNN_engine import *
from face.detection.opencv_engine import *
from face.recognition.facenet_engine import *
from object.inception_engine import *

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
            self.__faceDetectionEngine = OpenCVFaceEngine("engine")
        elif(config['face_detection'] == 'openface_engine'):
            self.__faceDetectionEngine = None
        elif(config['face_detection'] == 'MTCNN_engine'):
            self.__faceDetectionEngine = MTCNNFaceEngine("")

        # face data directory
        self.__face_data_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'+face_data_dir
        self.__face_model = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/resources/facenet/20170512-110547/20170512-110547.pb'
        self.__face_classifier = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/resources/facenet/face_classifier.pkl'
        #face recogition engine
        if(config['face_recognition'] == 'facenet'):
            self.__faceRecognitionEngine = FacenetEngine(
                            image_size=160,
                            data_dir=self.__face_data_dir,
                            classifier_filename=self.__face_classifier,
                            model=self.__face_model,
                            classifier_type=FacenetEngine.NEURAL_NETWORK, #LINEAR_SVM, RBF_SVM, DECISION_TREE, RANDOM_FOREST, NEURAL_NETWORK, ADA_BOOST
                            max_features=None,#None, auto, sqrt, log2
                            max_depth=5, n_estimators=100,
                            hidden_layer_sizes=(1000, 200))

        #object detection and recognition engine
        if(config['object_detection_recognition'] == 'yolo'):
            self.__objectEngine = None
        if(config['object_detection_recognition'] == 'inception'):
            self.__objectEngine = InceptionEngine(
                            model_dir='engine/cv/resources/inception',
                            num_top_predictions=10)


        print("Engine Created:")
        print("Face Detection Engine: ")
        print(self.__faceDetectionEngine)
        print("Face Recognition Engine: ")
        print(self.__faceRecognitionEngine)
        print("Object Engine: ")
        print(self.__objectEngine)

    def store_face_training_data(self, img, rects, img_name):
        '''store_training_data
        takes params
        img: image numpy array processed image
        rects: array of objects every object represent a rectangle with x, y, w, h and name of an object
        image_name: String image name to store the face images
        '''
        #checking if the name is none or empty
        if(img_name == None or img_name == ""):
            return

        # spliting img name and getting the name without the extention
        name_parts = img_name.split('.')
        if(len(name_parts) > 0):
            img_name = name_parts[0]

        # face data directory
        data_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+'/'+face_data_dir

        print ("Saving image faces to folder: ")
        print (data_dir)

        for i in range(len(rects)):
            # the processed rectangle
            rect = rects[i]

            # face image name
            face_name = img_name+'_'+str(i)+'.jpg'
            # folder name
            folder_name = data_dir+'/'+rect['name']
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            # cropping the face image
            face_img = img[rect['y']:rect['y']+rect['h'], rect['x']:rect['x']+rect['w']]

            # writing image to folder
            face_img = cv2.resize(face_img, (face_image_size, face_image_size))
            cv2.imwrite(folder_name+'/'+face_name, face_img)

        print("Finished saving training data")

        print("Training Classifier")
        self.__faceRecognitionEngine.train()
        print("Training Finished")


    def processImage(self, img):

        img, face_images, faces_rects = self.__faceDetectionEngine.detect_faces(img)

        # img_name = "IMG_0979"
        # person_name = 'aziz'
        # if not os.path.exists(self.__face_data_dir+'/'+person_name):
        #     os.mkdir(self.__face_data_dir+'/'+person_name)
        #
        # face_count = 0
        # for face in face_images:
        #     face = cv2.resize(face, (160, 160))
        #     # cv2.imwrite(self.__face_data_dir+'/'+person_name+'/'+img_name+'_face_'+str(face_count)+'.jpg', face)
        #     # face_count = face_count+1
        #     cv2.imshow("face", face)
        #     cv2.waitKey(0)

        # for face in face_images:
        face_predictions = self.__faceRecognitionEngine.predict_proba(face_images)

        # adding the predicted class names to face rectangles
        faces = []
        for i in range(len(face_predictions)):
            temp_rect = faces_rects[i]
            temp_rect['name'] = face_predictions[i]
            faces.append(temp_rect)

        # getting object classes from image
        objects = self.__objectEngine.predict_proba(img)

        data = {'faces': faces,'objects': objects}
        return data
