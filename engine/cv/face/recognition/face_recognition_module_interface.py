import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GlobalEntities import *

import numpy as np
import cv2

class FaceRecognitionInterface:
    def train(self): pass

    def predict_proba(self, img): pass

    '''store_training_data
    static method
    takes params
    img: image numpy array processed image
    rects: array of objects every object represent a rectangle with x, y, w, h and name of an object
    image_name: String image name to store the face images
    '''
    @staticmethod
    def store_training_data(img, rects, img_name):
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
