import numpy as np
import cv2

class FaceInterface:
    def detect_faces(self, img):  pass

    def number_of_faces(self, img):
        """ returns number of faces in the image (integer) """
        [img, faces, faces_rects] = self.detect_faces(img)
        return len(faces)

    def crop_faces(self, img):
        """ returns array of cropped faces every element is an image of a face """
        [img, face_images, faces_rects] = self.detect_faces(img)
        # for f in face_images:
        #     cv2.imshow("face", f)
        #     cv2.waitKey(0)
        return [img, face_images, faces_rects]
