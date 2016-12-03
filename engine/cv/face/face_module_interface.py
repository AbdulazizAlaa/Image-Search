import numpy as np
import cv2

class FaceInterface:
    def detect_faces(self, img):  pass

    def number_of_faces(self, img):
        """ returns number of faces in the image (integer) """
        faces = self.detect_faces(img)
        return len(faces)

    def crop_faces(self, img):
        """ returns array of cropped faces every element is an image of a face """
        faces = self.detect_faces(img)
        for f in faces:
            cv2.imshow("face", f)
            cv2.waitKey(0)
        return faces

