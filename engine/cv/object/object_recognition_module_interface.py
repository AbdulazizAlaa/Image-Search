import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GlobalEntities import *

import numpy as np
import cv2

class ObjectRecognitionInterface:
    def predict_proba(self, img): pass
