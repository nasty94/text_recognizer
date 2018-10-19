import cv2
from keras.models import load_model
import numpy as np


class CnnRecognizer:
    def __init__(self):
        self.model = load_model('models/cnn.h5')
        self.model._make_predict_function()
        self.counter = 0

    def recognize_number(self, images):
        images = CnnRecognizer.__image_pre_processing(images)
        return self.model.predict_classes(images)

    @staticmethod
    def __image_pre_processing(images):
        for i in range(len(images)):
            images[i] = cv2.resize(images[i], (48, 64))
            # images[i] = cv2.cvtColor(images[i], cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(images[i], (3, 3), 0)
            bw, threshold = cv2.threshold(blur, 1, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            images[i] = cv2.Canny(blur, bw / 2, bw)
        np_images = np.array(images)
        np_images = np_images.reshape(-1, 64, 48, 1)
        return np_images
