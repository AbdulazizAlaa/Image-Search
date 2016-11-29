import cv2

def detect_faces(img):
    """ returns array of face Rects. each rect represents a face. """
    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print "detect_faces"

def number_of_faces(img):
    """ returns number of faces in the image (integer) """
    print "number_of_faces"

def crop_faces(img):
    """ returns array of cropped faces every element is an image of a face """
    print "crop_faces"
