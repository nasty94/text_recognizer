from imutils.object_detection import non_max_suppression
import numpy as np
import pytesseract
import argparse
import cv2
import time
import imutils
from imutils import contours
import matplotlib.pyplot as plt
from socket import *

from Controller.CnnRecognizer import CnnRecognizer
from ImageReceiver import ImageReceiver

i = 0
cnn_recognizer = CnnRecognizer()


def view_image(image_arr: map, metadata: dict, _socket: socket):
    print("Image Received")
    arr = np.array(image_arr).astype(np.uint8)
    width = int(metadata["width"])
    height = int(metadata["height"])

    arr.resize((height, width), refcheck=False)
    image = cv2.resize(arr, dsize=(width * 3, height * 3))
    cnn_recognizer.counter += 1

    thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    serial_contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
    serial_contours = contours.sort_contours(serial_contours, method="left-to-right")[0]

    serial = []
    if len(serial_contours) > 7:
        (x, y, w, h) = cv2.boundingRect(serial_contours[-7])
        roi = image[:, :x]
        serial = image[:, x - 10:]
        # cv2.imwrite("r.jpg", roi)
        # cv2.imwrite("d.jpg", serial)

    # for debugging
    # cv2.imwrite("s.jpg", image)
    text = ""
    if i == 0:
        config = "-l ara_number"
        text = pytesseract.image_to_string(serial, config=config)
    elif i == 1:
        text = str(cnn_recognizer.recognize_number([image])[0])
    print("number: " + text)
    _socket.send((text + "\n").encode())
    _socket.close()


def file_received_call_back(data, metadata: dict, _socket: socket):
    view_image(data, metadata, _socket)


receiver = ImageReceiver(file_received_call_back)
receiver.start_connection()
