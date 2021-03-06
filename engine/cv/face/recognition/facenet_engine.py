import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from face.recognition.face_recognition_module_interface import *
from GlobalEntities import *

import face.recognition.facenet as facenet
from face.recognition.augmentation import augment

from scipy import misc
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier

import tensorflow as tf
from tensorflow.python.framework import ops

import numpy as np
import os
import sys
import math
import pickle
import cv2


class FacenetEngine(FaceRecognitionInterface):
    LINEAR_SVM = 'linear_svm'
    RBF_SVM = 'rbf_svm'
    DECISION_TREE = 'decision_tree'
    RANDOM_FOREST = 'random_forest'
    NEURAL_NETWORK = 'fully_connected'
    ADA_BOOST = 'ada_boost'
    def __init__(self, data_dir, classifier_filename, model, classifier_type=LINEAR_SVM,
                seed=666, use_split_dataset=True, image_size=160, batch_size=90,
                min_nrof_images_per_class=20, nrof_train_images_per_class=10,
                max_depth=5, n_estimators=10, max_features=1,
                hidden_layer_sizes=(100,)):
        self.__seed = seed
        self.__use_split_dataset = use_split_dataset
        self.__data_dir = data_dir
        self.__min_nrof_images_per_class = min_nrof_images_per_class
        self.__nrof_train_images_per_class = nrof_train_images_per_class
        self.__image_size = image_size
        self.__batch_size = batch_size
        self.__classifier_filename = classifier_filename
        self.__model = model
        self.__classifier_type = classifier_type

        # self.__classifiers = { 'linear_svm' : SVC(kernel="linear", C=0.025, probability=True),
        #                         'rbf_svm' : SVC(gamma=2, C=1, probability=True),
        #                         'decision_tree' : DecisionTreeClassifier(max_depth=max_depth),
        #                         'random_forest' : RandomForestClassifier(max_depth=max_depth, n_estimators=n_estimators, max_features=max_features),
        #                         'fully_connected' : MLPClassifier(alpha=1, hidden_layer_sizes=hidden_layer_sizes),
        #                         'ada_boost' : AdaBoostClassifier(n_estimators=n_estimators)}

        # self.__classifier = self.__classifiers[classifier_type]
        self.__classifier = RandomForestClassifier(n_estimators=n_estimators, n_jobs=7)


    def train(self):
        with tf.Graph().as_default():

            with tf.Session() as sess:

                np.random.seed(seed=self.__seed)

                dataset = facenet.get_dataset(self.__data_dir)

                # Check that there are at least one training image per class
                for cls in dataset:
                    assert(len(cls.image_paths)>0, 'There must be at least one image for each class in the dataset')

                # TODO remove this read dataset
                paths, labels = facenet.get_image_paths_and_labels(dataset)

                # print(self.__data_dir)
                # images_list, labels = augment(self.__data_dir, 50)
                #
                # print(len(images_list))

                print('Number of classes: %d' % len(dataset))
                print('Number of images: %d' % len(paths))
                # print('Number of images: %d' % len(images_list))

                # Load the model
                print('Loading feature extraction model')
                facenet.load_model(self.__model)

                # Get input and output tensors
                images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
                embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
                phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
                embedding_size = embeddings.get_shape()[1]

                # Run forward pass to calculate embeddings
                print('Calculating features for images')
                nrof_images = len(paths)
                # nrof_images = len(images_list)
                nrof_batches_per_epoch = int(math.ceil(1.0*nrof_images / self.__batch_size))
                emb_array = np.zeros((nrof_images, embedding_size))

                for i in range(nrof_batches_per_epoch):
                    start_index = i*self.__batch_size
                    end_index = min((i+1)*self.__batch_size, nrof_images)
                    paths_batch = paths[start_index:end_index]

                    # images = images_list[start_index:end_index]
                    images = facenet.load_data(paths_batch, False, False, self.__image_size)

                    feed_dict = { images_placeholder:images, phase_train_placeholder:False }
                    emb_array[start_index:end_index,:] = sess.run(embeddings, feed_dict=feed_dict)

                classifier_filename_exp = os.path.expanduser(self.__classifier_filename)

                # Train classifier
                print('Training classifier')
                self.__classifier.fit(emb_array, labels)

                # Create a list of class names
                class_names = [ cls.name.replace('_', ' ') for cls in dataset]

                # Saving classifier model
                with open(classifier_filename_exp, 'wb') as outfile:
                    pickle.dump((self.__classifier, class_names), outfile)
                print('Saved classifier model to file "%s"' % classifier_filename_exp)


    def predict_proba(self, imgs):
        if(len(imgs) == 0):
            print('no faces to process.')
            return []
        with tf.Graph().as_default():

            with tf.Session() as sess:

                np.random.seed(seed=self.__seed)


                # Load the model
                print('Loading feature extraction model')
                facenet.load_model(self.__model)

                # Get input and output tensors
                images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
                embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
                phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
                embedding_size = embeddings.get_shape()[1]

                # Run forward pass to calculate embeddings
                print('Calculating features for images')
                images = facenet.load_data(imgs, False, False, self.__image_size)
                # images = np.zeros((len(imgs), self.__image_size, self.__image_size, 3), dtype='uint8')
                # # imgs = np.asarray(imgs)
                # for i in range(len(imgs)):
                #     # cv2.imshow('before', imgs[i])
                #
                #     w, h, c = imgs[i].shape
                #     if w>self.__image_size or h>self.__image_size :
                #         zero_image = cv2.resize(imgs[i], (self.__image_size, self.__image_size))
                #     else:
                #         zero_image = np.ones((self.__image_size, self.__image_size, 3), dtype='uint8')
                #         zero_image[0:w, 0:h, :] = imgs[i]
                #
                #
                #     # cv2.imshow('after', zero_image)
                #     # cv2.waitKey(0)
                #     images[i, :, :, :] = zero_image[:, :, :]

                # face_predictions = []
                feed_dict = { images_placeholder:images, phase_train_placeholder:False }
                emb_array = sess.run(embeddings, feed_dict=feed_dict)

                classifier_filename_exp = os.path.expanduser(self.__classifier_filename)

                # Classify images
                print('Testing classifier')
                with open(classifier_filename_exp, 'rb') as infile:
                    (self.__classifier, class_names) = pickle.load(infile)
                print (class_names)

                print('Loaded classifier model from file "%s"' % classifier_filename_exp)

                # emb_array = np.load("/home/abdulaziz/workspace/Machine Learning/graduation_project/engine/cv/data/face_images_embeddings.npy")

                predictions = self.__classifier.predict_proba(emb_array)
                best_class_indices = np.argmax(predictions, axis=1)
                best_class_probabilities = predictions[np.arange(len(best_class_indices)), best_class_indices]

                # getting the predictions
                face_predictions = []
                for i in range(len(best_class_indices)):
                    name_parts = class_names[best_class_indices[i]].split(" ")
                    name = ''
                    user_flag = False
                    if(len(name_parts) == 2):
                        name = name_parts[0]
                        user_flag = (name_parts[1] == 0)
                    elif(len(name_parts) > 0):
                        name = name_parts[0]
                        user_flag = False

                    face_predictions.append({'name': name, 'probability':best_class_probabilities[i], 'user_flag': user_flag})
                    print('%4d %s: %.3f' %
                    (i, class_names[best_class_indices[i]], best_class_probabilities[i]))

                return face_predictions
