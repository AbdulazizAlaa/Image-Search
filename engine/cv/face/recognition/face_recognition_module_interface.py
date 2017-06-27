import numpy as np
import cv2

class FaceRecognitionInterface:
    def predict_proba(self, img): pass

    def predict_probas(self, imgs):
        for img in imgs:
            self.predict_proba(img)
