from imutils.object_detection import non_max_suppression
import numpy as np
import pytesseract
import argparse
import cv2
import time
import matplotlib.pyplot as plt
from socket import *

from ImageReceiver import ImageReceiver


def view_image(image_arr: map, metadata: dict, _socket: socket):
    print("Image Received")
    arr = np.array(image_arr).astype(np.uint8)
    width = int(metadata["width"])
    height = int(metadata["height"])
    arr.resize((height, width), refcheck=False)
    image = cv2.resize(arr, dsize=(width * 3, height * 3))
    config = "-l ara_number"
    text = pytesseract.image_to_string(image, config=config)
    print("number: " + text)
    _socket.send((text + "\n").encode())
    _socket.close()


def file_received_call_back(data, metadata: dict, _socket : socket):
    view_image(data, metadata, _socket)
    pass


receiver = ImageReceiver(file_received_call_back)
receiver.start_connection()
