import glob
import os.path
import random

import cv2
import numpy as np
from imgaug import augmenters as iaa

import CONSTANT

'''
    класс карт: 
0-нет
1-шальная
2-заводила
3-наворот
4-приход
5-карта дохлого
6-сокровище

        тип:
0-нет/без типа
1-кумар
2-мрак
3-порча
4-трава
5-угар

    карта:
0-нет
1-25 - номер в типе
'''

seq = iaa.Sequential([
    iaa.Sometimes(0.5, iaa.CoarseDropout((0.01, 0.15), size_percent=0.1)),
    iaa.Sometimes(0.5, iaa.GaussianBlur(sigma=(0.0, 0.5))),
    iaa.Sometimes(0.5, iaa.PerspectiveTransform(scale=(0.01, 0.2))),
    iaa.Sometimes(0.3, iaa.BlendAlphaCheckerboard(nb_rows=2, nb_cols=(1, 4),
                                                  foreground=iaa.AddToHue((-100, 100)))),
    iaa.Sometimes(0.5, iaa.Rotate((-45, 45))),
    #
    iaa.ScaleX((0.7, 1)),
    iaa.ScaleY((0.7, 1))
])


def prepare_imgs(filenames):
    return [prepare_img(x) for x in filenames]


def prepare_img(filename: str):
    file_is_exist = os.path.exists(filename)
    file_is_exist = file_is_exist and os.path.isfile(filename)
    if not file_is_exist:
        return None
    img = cv2.imread(filename)[..., ::-1]

    img = cv2.resize(img, CONSTANT.INPUT_IMAGE_SHAPE[:2])
    return img


def get_label(label):
    return CONSTANT.DATASET_LABEL[label-1]


def get_index(file_path):
    basename = os.path.basename(file_path)
    filename = os.path.splitext(basename)[0]
    filename = filename.split("_")[0]
    return CONSTANT.DATASET_LABEL.index(filename) + 1


def get_data():
    data = glob.glob("%s/*" % CONSTANT.DATASET_FOLDER)
    data_len = len(data)
    data = {k + 1: v for k, v in enumerate(data)}
    return data, data_len


def data_gen(data=None, data_len=94, batch_size=256, aug=False):
    if not data:
        data, data_len = get_data()

    x = list()
    y = list()

    while True:
        while len(x) < batch_size:
            index, i = random.choice(list(data.items()))
            one_hot = np.zeros(data_len + 1)
            one_hot[index] = 1
            img = cv2.imread(i)[..., ::-1]

            img = cv2.resize(img, (128, 256))
            x.append(img)
            y.append(one_hot)

        x = np.stack(x, axis=0)
        y = np.stack(y, axis=0)

        if aug:
            x = seq(images=x)

        yield x, y
