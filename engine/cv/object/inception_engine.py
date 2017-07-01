# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Simple image classification with Inception.

Run image classification with Inception trained on ImageNet 2012 Challenge data
set.

This program creates a graph from a saved GraphDef protocol buffer,
and runs inference on an input JPEG image. It outputs human readable
strings of the top 5 predictions along with their probabilities.

Change the --image_file argument to any jpg image to compute a
classification of that image.

Please see the tutorial and website for a detailed description of how
to use this script to perform image recognition.

https://tensorflow.org/tutorials/image_recognition/
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
sys.path.insert(0, "..")

import os
import os.path
import sys
import tarfile

import numpy as np
from six.moves import urllib
import tensorflow as tf

from engine.cv.object.object_recognition_module_interface import *
from engine.cv.object.node_lookup import *

class InceptionEngine(ObjectRecognitionInterface):
    def __init__(self, model_dir='engine/cv/resources/inception', num_top_predictions=10, threshold=.2):
        self.__num_top_predictions = num_top_predictions
        self.__model_dir = model_dir
        self.__DATA_URL = 'http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz'
        self.__threshold = threshold
        
        # download and extract model file if not present
        self.maybe_download_and_extract()

    def maybe_download_and_extract(self):
        """Download and extract model tar file."""
        if not os.path.exists(self.__model_dir):
            os.makedirs(self.__model_dir)
        filename = self.__DATA_URL.split('/')[-1]
        filepath = os.path.join(self.__model_dir, filename)
        if not os.path.exists(os.path.join(self.__model_dir, 'classify_image_graph_def.pb')):
            def _progress(count, block_size, total_size):
                sys.stdout.write('\r>> Downloading %s %.1f%%' % (
                filename, float(count * block_size) / float(total_size) * 100.0))
                sys.stdout.flush()
            filepath, _ = urllib.request.urlretrieve(self.__DATA_URL, filepath, _progress)
            print()
            statinfo = os.stat(filepath)
            print('Successfully downloaded', filename, statinfo.st_size, 'bytes.')
            tarfile.open(filepath, 'r:gz').extractall(self.__model_dir)
            os.remove(os.path.join(self.__model_dir, 'cropped_panda.jpg'))
            os.remove(filepath)


    def create_graph(self):
        """Creates a graph from saved GraphDef file and returns a saver."""
        # Creates graph from saved graph_def.pb.
        with tf.gfile.FastGFile(os.path.join(
            self.__model_dir, 'classify_image_graph_def.pb'), 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(graph_def, name='')

    def predict_proba(self, image):
        """Runs inference on an image.

        Args:
        image: Image numpy array.

        Returns:
        Nothing
        """
        # Creates graph from saved GraphDef.
        self.create_graph()

        with tf.Session() as sess:
            # Some useful tensors:
            # 'softmax:0': A tensor containing the normalized prediction across
            #   1000 labels.
            # 'pool_3:0': A tensor containing the next-to-last layer containing 2048
            #   float description of the image.
            # 'DecodeJpeg/contents:0': A tensor containing a string providing JPEG
            #   encoding of the image.
            # Runs the softmax tensor by feeding the image_data as input to the graph.
            softmax_tensor = sess.graph.get_tensor_by_name('softmax:0')

            #encode image into jpeg encoding
            image = tf.image.encode_jpeg(image)
            image_data = tf.convert_to_tensor(image).eval()

            predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})
            predictions = np.squeeze(predictions)

            # Creates node ID --> English string lookup.
            node_lookup = NodeLookup(model_dir='engine/cv/resources/inception')

            # TODO only return over some threshold
            objects = []
            top_k = predictions.argsort()[-self.__num_top_predictions:][::-1]
            for node_id in top_k:
                score = predictions[node_id]
                if(score > self.__threshold):
                    human_string = node_lookup.id_to_string(node_id)
                    for obj in human_string.split(','):
                        objects.append(obj)
                    print('%s (score = %.5f)' % (human_string, score))

            return objects
