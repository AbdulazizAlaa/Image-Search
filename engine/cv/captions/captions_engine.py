import sys
sys.path.insert(0, "..")

import tensorflow as tf
import numpy as np
import pandas as pd
import os
import cv2

import tensorflow.python.platform

from engine.cv.captions.caption_generator import *

class CaptionsEngine():
    def __init__(self,
                dim_embed = 256,
                dim_hidden = 256,
                dim_in = 4096,
                batch_size = 1,
                learning_rate = 0.001,
                momentum = 0.9,
                n_epochs = 25,
                model_path = 'engine/cv/resources/captions/models/tensorflow',
                vgg_path = 'engine/cv/resources/captions/data/vgg16-20160129.tfmodel',
                words_model = 'engine/cv/resources/captions/data/ixtoword.npy'):
        self.__dim_embed = dim_embed
        self.__dim_hidden = dim_hidden
        self.__dim_in = dim_in
        self.__batch_size = batch_size
        self.__learning_rate = learning_rate
        self.__momentum = momentum
        self.__n_epochs = n_epochs

        self.__model_path = model_path
        self.__vgg_path = vgg_path
        self.__words_model = words_model

        if not os.path.exists(self.__words_model):
            print ('You must run Training first.')
        else:
            tf.reset_default_graph()
            with open(vgg_path,'rb') as f:
                fileContent = f.read()
                graph_def = tf.GraphDef()
                graph_def.ParseFromString(fileContent)

            self.__images = tf.placeholder("float32", [1, 224, 224, 3])
            tf.import_graph_def(graph_def, input_map={"images":self.__images})

            self.__ixtoword = np.load(self.__words_model).tolist()
            n_words = len(self.__ixtoword)
            maxlen=15
            self.__graph = tf.get_default_graph()
            self.__sess = tf.InteractiveSession(graph=self.__graph)
            caption_generator = Caption_Generator(self.__dim_in, self.__dim_hidden, self.__dim_embed, self.__batch_size, maxlen+2, n_words)
            self.__graph = tf.get_default_graph()

            self.__image, self.__generated_words = caption_generator.build_generator(maxlen=maxlen)

    def crop_image(self, image, target_height=227, target_width=227, as_float=True):
        if as_float:
            image = image.astype(np.float32)

        if len(image.shape) == 2:
            image = np.tile(image[:,:,None], 3)
        elif len(image.shape) == 4:
            image = image[:,:,:,0]

        height, width, rgb = image.shape
        if width == height:
            resized_image = cv2.resize(image, (target_height,target_width))

        elif height < width:
            resized_image = cv2.resize(image, (int(width * float(target_height)/height), target_width))
            cropping_length = int((resized_image.shape[1] - target_height) / 2)
            resized_image = resized_image[:,cropping_length:resized_image.shape[1] - cropping_length]

        else:
            resized_image = cv2.resize(image, (target_height, int(height * float(target_width) / width)))
            cropping_length = int((resized_image.shape[0] - target_width) / 2)
            resized_image = resized_image[cropping_length:resized_image.shape[0] - cropping_length,:]

        return cv2.resize(resized_image, (target_height, target_width))

    def read_image(self, image):

         img = self.crop_image(image, target_height=224, target_width=224)
         if img.shape[2] == 4:
             img = img[:,:,:3]

         img = img[None, ...]
         return img

    def generate_caption(self, image): # Naive greedy search

        feat = self.read_image(image)
        fc7 = self.__sess.run(self.__graph.get_tensor_by_name("import/Relu_1:0"), feed_dict={self.__images:feat})

        saver = tf.train.Saver()
        sanity_check=False
        # sanity_check=True
        if not sanity_check:
            saved_path=tf.train.latest_checkpoint(self.__model_path)
            saver.restore(self.__sess, saved_path)
        else:
            tf.global_variables_initializer().run()

        generated_word_index= self.__sess.run(self.__generated_words, feed_dict={self.__image:fc7})
        generated_word_index = np.hstack(generated_word_index)
        self.__generated_words = [self.__ixtoword[x] for x in generated_word_index]
        punctuation = np.argmax(np.array(self.__generated_words) == '.')+1

        self.__generated_words = self.__generated_words[:punctuation]
        generated_sentence = ' '.join(self.__generated_words)

        print(generated_sentence)

        return generated_sentence
