import sys
sys.path.insert(0, "..")

import tensorflow as tf
import numpy as np
import pandas as pd
import os
import cv2

import tensorflow.python.platform

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

class Caption_Generator():
    def __init__(self, dim_in, dim_embed, dim_hidden, batch_size, n_lstm_steps, n_words, init_b=None):

        self.dim_in = dim_in
        self.dim_embed = dim_embed
        self.dim_hidden = dim_hidden
        self.batch_size = batch_size
        self.n_lstm_steps = n_lstm_steps
        self.n_words = n_words

        # declare the variables to be used for our word embeddings
        with tf.device("/cpu:0"):
            self.word_embedding = tf.Variable(tf.random_uniform([self.n_words, self.dim_embed], -0.1, 0.1), name='word_embedding')

        self.embedding_bias = tf.Variable(tf.zeros([dim_embed]), name='embedding_bias')

        # declare the LSTM itself
        self.lstm = tf.contrib.rnn.BasicLSTMCell(dim_hidden)

        # declare the variables to be used to embed the image feature embedding to the word embedding space
        self.img_embedding = tf.Variable(tf.random_uniform([dim_in, dim_hidden], -0.1, 0.1), name='img_embedding')
        self.img_embedding_bias = tf.Variable(tf.zeros([dim_hidden]), name='img_embedding_bias')

        # declare the variables to go from an LSTM output to a word encoding output
        self.word_encoding = tf.Variable(tf.random_uniform([dim_hidden, n_words], -0.1, 0.1), name='word_encoding')

        # optional initialization setter for encoding bias variable
        if init_b is not None:
            self.word_encoding_bias = tf.Variable(init_b, name='word_encoding_bias')
        else:
            self.word_encoding_bias = tf.Variable(tf.zeros([n_words]), name='word_encoding_bias')

    def build_model(self):
        # declaring the placeholders for our extracted image feature vectors, our caption, and our mask
        # (describes how long our caption is with an array of 0/1 values of length `maxlen`
        img = tf.placeholder(tf.float32, [self.batch_size, self.dim_in])
        caption_placeholder = tf.placeholder(tf.int32, [self.batch_size, self.n_lstm_steps])
        mask = tf.placeholder(tf.float32, [self.batch_size, self.n_lstm_steps])

        # getting an initial LSTM embedding from our image_imbedding
        image_embedding = tf.matmul(img, self.img_embedding) + self.img_embedding_bias

        # setting initial state of our LSTM
        state = self.lstm.zero_state(self.batch_size, dtype=tf.float32)

        total_loss = 0.0
        with tf.variable_scope("RNN"):
            for i in range(self.n_lstm_steps):
                if i > 0:
                   #if this isn’t the first iteration of our LSTM we need to get the word_embedding corresponding
                   # to the (i-1)th word in our caption
                    with tf.device("/cpu:0"):
                        current_embedding = tf.nn.embedding_lookup(self.word_embedding, caption_placeholder[:,i-1]) + self.embedding_bias
                else:
                     #if this is the first iteration of our LSTM we utilize the embedded image as our input
                    current_embedding = image_embedding
                if i > 0:
                    # allows us to reuse the LSTM tensor variable on each iteration
                    tf.get_variable_scope().reuse_variables()

                out, state = self.lstm(current_embedding, state)


                if i > 0:
                    #get the one-hot representation of the next word in our caption
                    labels = tf.expand_dims(caption_placeholder[:, i], 1)
                    ix_range=tf.range(0, self.batch_size, 1)
                    ixs = tf.expand_dims(ix_range, 1)
                    concat = tf.concat([ixs, labels],1)
                    onehot = tf.sparse_to_dense(
                            concat, tf.stack([self.batch_size, self.n_words]), 1.0, 0.0)


                    #perform a softmax classification to generate the next word in the caption
                    logit = tf.matmul(out, self.word_encoding) + self.word_encoding_bias
                    xentropy = tf.nn.softmax_cross_entropy_with_logits(logits=logit, labels=onehot)
                    xentropy = xentropy * mask[:,i]

                    loss = tf.reduce_sum(xentropy)
                    total_loss += loss

            total_loss = total_loss / tf.reduce_sum(mask[:,1:])
            return total_loss, img,  caption_placeholder, mask


    def build_generator(self, maxlen, batchsize=1):
        #same setup as `build_model` function
        img = tf.placeholder(tf.float32, [self.batch_size, self.dim_in])
        image_embedding = tf.matmul(img, self.img_embedding) + self.img_embedding_bias
        state = self.lstm.zero_state(batchsize,dtype=tf.float32)

        #declare list to hold the words of our generated captions
        all_words = []
        with tf.variable_scope("RNN"):
            # in the first iteration we have no previous word, so we directly pass in the image embedding
            # and set the `previous_word` to the embedding of the start token ([0]) for the future iterations
            output, state = self.lstm(image_embedding, state)
            previous_word = tf.nn.embedding_lookup(self.word_embedding, [0]) + self.embedding_bias

            for i in range(maxlen):
                tf.get_variable_scope().reuse_variables()

                out, state = self.lstm(previous_word, state)


                # get a one-hot word encoding from the output of the LSTM
                logit = tf.matmul(out, self.word_encoding) + self.word_encoding_bias
                best_word = tf.argmax(logit, 1)

                with tf.device("/cpu:0"):
                    # get the embedding of the best_word to use as input to the next iteration of our LSTM
                    previous_word = tf.nn.embedding_lookup(self.word_embedding, best_word)

                previous_word += self.embedding_bias

                all_words.append(best_word)

        return img, all_words
