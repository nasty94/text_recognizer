import cv2
from keras.models import load_model
import numpy as np
def recognize_number(images ):
   
    images =  image_pre_processing(images)
    model = load_model('models/cnn.h5')
    predictions = model.predict_classes(images)



def image_pre_processing(images):
    for i in range(len(images)):
        images[i] = cv2.resize(images[i], (48, 64))
        images[i] = cv2.cvtColor(images[i], cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(images[i], (3, 3), 0)
        bw , threshold = cv2.threshold(blur, 1, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        images[i] = cv2.Canny(blur,bw/2,bw)
    np_images = np.array(images)
    np_images = np_images.reshape(-1, 64, 48, 1)
    return np_images

