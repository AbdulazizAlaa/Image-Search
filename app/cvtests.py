import sys
sys.path.insert(0, "..")

from engine.cv.vision import vision_engine

import numpy as np
import cv2
import os
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

def detect_faces_save_face_crops(data_dir):
    for folder in os.listdir(data_dir):

        if os.path.isfile(folder):
            continue
        print(folder)

        images_dir = os.path.join(data_dir, folder)
        i = 0

        for image_file in os.listdir(images_dir):
            image_file_path = os.path.join(images_dir, image_file)

            if not os.path.isfile(image_file_path):
                continue

            print(image_file)

            img = cv2.imread(image_file_path, 1)
            face_images, face_rects = engine.detect_faces(img)
            os.remove(image_file_path)

            face_image_size = 160
            for face_img in face_images:
                # writing image to folder
                face_img = cv2.resize(face_img, (face_image_size, face_image_size))
                cv2.imwrite(os.path.join(images_dir, str(i)+".jpg"), face_img)
                i=i+1
                # cv2.imshow("face", face_img)
                # cv2.waitKey(0)


# Load an color image in grayscale
# img = cv2.imread('/home/abdulaziz/Downloads/testcases/1.jpg',1) #change this with any other image on your computer
# img = cv2.imread('/home/abdulaziz/workspace/Machine Learning/graduation_project/aziz.jpg', 1) #change this with any other image on your computer
# img = cv2.imread('/home/abdulaziz/Downloads/test/obj2.jpg',1) #change this with any other image on your computer
# img = cv2.imread('/home/abdulaziz/Downloads/testcases/6.jpg',1) #change this with any other image on your computer

# creating engine instance
engine = vision_engine.VisionEngine({'face_detection': 'MTCNN_engine',
                                    'face_recognition': 'facenet',
                                    'object_detection_recognition': False,
                                    'captions_generation_engine': False})
# # example use method store faces
# # is used after Successfully tagging image by user so it can be used for training
# engine.store_face_training_data(img, [{'name': 'aziz', 'x': 424, 'h': 393, 'y': 188, 'w': 313}], "aziz.jpg")

# data_dir = "/home/abdulaziz/workspace/Machine Learning/graduation_project/engine/cv/data/"
# detect_faces_save_face_crops(data_dir)

# # trianing face clssifier
# engine.train_face_classifier()

# predict
image_file = "/home/abdulaziz/Downloads/test/2.jpg"
# image_file = "/home/abdulaziz/Downloads/test/data_/aziz/14380068_1247424745298684_3461037652182148485_o.jpg"

img_cv = cv2.imread(image_file,1)

face_images, face_rects = engine.detect_faces(img_cv)
face_image_size = 160
images_dir = "/home/abdulaziz/workspace/Machine Learning/graduation_project/engine/cv/data_face"

for face, rect in zip(face_images, face_rects):
    face_img = cv2.resize(face, (face_image_size, face_image_size))
    name = str(rect['x'])+","+str(rect['y'])+","+str(rect['w'])+","+str(rect['h'])+".jpg"
    cv2.imwrite(os.path.join(images_dir, name), face_img)


#folder to save the output of the augmentation
paths = []
rects = []
for image_file in os.listdir(images_dir):
    image_file_path = os.path.join(images_dir, image_file)

    if not os.path.isfile(image_file_path):
        continue

    paths.append(image_file_path)

    parts = image_file.split('.')
    parts = parts[0].split(',')
    rects.append({'x':parts[0], 'y':parts[1], 'w':parts[2], 'h':parts[3]})

face_predictions = engine.predict_face(paths)

for image_file in os.listdir(images_dir):
    image_file_path = os.path.join(images_dir, image_file)
    os.remove(image_file_path)

cv2.namedWindow('face', cv2.WINDOW_NORMAL)
for face, prediction in zip(rects, face_predictions):

    cv2.rectangle(img_cv,(int(face['x']),int(face['y'])),(int(face['x'])+int(face['w']),int(face['y'])+int(face['h'])),(0,255,0),3)
    cv2.putText(img_cv, prediction['name'], (int(face['x']),int(face['y'])+int(face['h'])+20), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),5)
    cv2.putText(img_cv, str(int(prediction['probability']*100))+"%", (int(face['x']),int(face['y'])+int(face['h'])+5x0), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),4)

cv2.imshow('face', img_cv)
cv2.waitKey(0)

# # creating engine instance
# engine = vision_engine.VisionEngine({'face_detection': 'MTCNN_engine',
#                                     'face_recognition': 'facenet',
#                                     'object_detection_recognition': 'inception',
#                                     'captions_generation_engine': True})
# # example use method processImage
# # process Image and returns face rectangles and face predictions and object predictions
# print(engine.processImage(img))
