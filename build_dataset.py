import cv2
import numpy as np
import math
import time
import os

PATH_OBJECT_1 = "base_de_donnee/object_1/"
PATH_OBJECT_2 = "base_de_donnee/object_2/"

NUM_IMAGES_P_OBJECT = 1000

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    cap.open()

def create_dataset_dirs():
    try:
        print("Creation du dossier base de donnees sur le meme repertoire que ce script.")
        os.makedirs(PATH_OBJECT_1)
        os.makedirs(PATH_OBJECT_2)
    except:
        print("Folders already exist")

def save_image_to_disk(img, object, name):
    """
        object: 1 means save PATH_OBJECT_1
                2 "" "" ""   PATH_OBJECT_2
        name: name to write to disk
    """
    path = PATH_OBJECT_1
    if object == 2:
        path = PATH_OBJECT_2
    name = path + name
    resized_img = cv2.resize(img,(224,224))
    cv2.imwrite(name, resized_img)

def pause(t=3):
    time.sleep(t)

def cleanup():
    cv2.destroyAllWindows()

def capture_image():
    ret, image = cap.read()
    image = cv2.flip(image,1)
    return image

def show_image(image):
    cv2.imshow('window', image)

def put_text(img, text, pos='bottom'):
    if pos == 'top':
        pos = (10, 50)
    else:
        pos = (10,450)
    font = cv2.FONT_HERSHEY_SIMPLEX
    return cv2.putText(img, text, pos, font, 0.7, (0, 255, 0), 2, cv2.LINE_AA)

def must_stop_capture():
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return True
    return False

def get_ready(text):
    text_top = text
    text_bottom = "Appuyer sur la touche 'q' si vous etes pret!"
    record_until_stopped(text_top, text_bottom)

def record_until_stopped(text_top, text_bottom):
    while True:
        image = capture_image()
        image = put_text(image, text_top, pos='top')
        image = put_text(image, text_bottom, pos='bottom')
        show_image(image)
        if must_stop_capture():
            break
    cleanup()

def record_images_for_object(object, num=10):
    for i in range(num):
        image = capture_image()
        img_name = str(i) + ".png"
        save_image_to_disk(image, object, img_name)
        text_top = "Images capturees: {}/{}".format(i, num)
        image = put_text(image, text_top, pos='top')
        # image = put_text(image, text_bottom, pos='bottom')
        show_image(image)
        if must_stop_capture():
            break
    cleanup()

if __name__ == "__main__":
    create_dataset_dirs()

    # Object 1
    get_ready("Positionner l'object 1 devant la camera")
    record_images_for_object(1, NUM_IMAGES_P_OBJECT)

    # Object 2
    get_ready("Positinner l'object 2 devant la camera")
    record_images_for_object(2, NUM_IMAGES_P_OBJECT)

    cap.release()