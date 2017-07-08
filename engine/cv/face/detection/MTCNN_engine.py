import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import resources.mtcnn.detect_face as detect_face

from face.detection.face_module_interface import *
from GlobalEntities import *

from scipy import misc
import tensorflow as tf
import numpy as np
import cv2

class MTCNNFaceEngine(FaceInterface):

    def __init__(self, engine):
        self.__engine = engine

    def detect_faces(self, img):
        """ returns array of face Rects and array of face mats. each entry represents a face. """
        with tf.Graph().as_default():
            gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=.7)
            sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
            with sess.as_default():
                pnet, rnet, onet = detect_face.create_mtcnn(sess, None)

        minsize = 20 # minimum size of face
        threshold = [ 0.6, 0.7, 0.7 ]  # three steps's threshold
        factor = 0.709 # scale factor

        bounding_boxes, _ = detect_face.detect_face(img, minsize, pnet, rnet, onet, threshold, factor)

        nrof_faces = bounding_boxes.shape[0]
        img_size = np.asarray(img.shape)[0:2]

        faces = []
        faces_rects = []

        for i in range(nrof_faces):
            det = bounding_boxes[i,0:4]
            bb = np.zeros(4, dtype=np.int32)
            bb[0] = np.maximum(det[0]-5/2, 0)
            bb[1] = np.maximum(det[1]-5/2, 0)
            bb[2] = np.minimum(det[2]+5/2, img_size[1])
            bb[3] = np.minimum(det[3]+5/2, img_size[0])
            faces.append(img[bb[1]:bb[3], bb[0]:bb[2], :])
            faces_rects.append({'name': 'none', 'x': bb[0], 'y': bb[1], 'w': bb[2]-bb[0], 'h': bb[3]-bb[1]})

        return [img, faces, faces_rects]
