from PIL.Image import open, fromarray
import numpy as np
import cv2
import os
import random as rd
import imagehash
def load_images(image_path):
    return np.array(open(image_path))

def gray_image(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image

def new_data_image(image):
    rotated_images = [
        cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE),
        cv2.rotate(image, cv2.ROTATE_180),
        cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    ]
    return rotated_images


def use_PIL(image):
    return fromarray(image)


def show(name, image, waitKey='q'):
    cv2.imshow(name, image)
    print(f"Image opened successfully")
    while True:
        if cv2.waitKey(1) & 0xFF == ord(waitKey):
            break
    # ปิดหน้าต่าง
    cv2.destroyAllWindows()
    print(f"closed image successfully")
    return

def adjust_img_color(image, number_new=1, color_value=0.5, color_value_end=1.5):
    list_img = []
    for _ in range(number_new+1):
        number = rd.uniform(color_value, color_value_end)
        if number != 1:
            list_img.append(cv2.convertScaleAbs(image, alpha=number))
    return list_img

def resize(image, size):
    return cv2.resize(image, size)

def save(name: str, file):
    try:
        cv2.imwrite(name, file)
        return True, None
    except Exception as e:
        return False, e

def BGR_TO_RGB(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def size(image):
    return image.size

def images_have_same_hash(img, image) -> bool:
    return imagehash.average_hash(use_PIL(resize(image, (300, 300)))) == imagehash.average_hash(use_PIL(resize(img, (300, 300))))

