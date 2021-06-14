import glob
import os.path
import random

import cv2
import numpy as np
from imgaug import augmenters as iaa

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
    iaa.Sometimes(0.5, iaa.CoarseDropout((0.01, 0.05), size_percent=0.05)),
    # iaa.Sometimes(0., iaa.GaussianBlur(sigma=(0.0, 0.5))),
    iaa.Sometimes(0.5, [iaa.PerspectiveTransform(scale=(0.01, 0.1))]),
    # iaa.Sometimes(0., iaa.Rot90(k=(1, 3))),
    #
    iaa.ScaleX((0.8, 1)),
    iaa.ScaleY((0.8, 1))
])


def prepeare_img(filename:str):
    file_is_exist = os.path.exists(filename)
    file_is_exist = file_is_exist and os.path.isfile(filename)
    if not file_is_exist:
        return None
    data = glob.glob(filename)
    img = cv2.imread(data)[..., ::-1]

    img = cv2.resize(img, (128, 256))
    return img



def data_gen(data=None, batch_size=256, aug=False):
    if not data:
        data = glob.glob('dataset\card\*')
        data = {k + 1: v for k, v in enumerate(data)}

    x = list()
    y = list()

    while True:
        while len(x) < batch_size:
            index, i = random.choice(list(data.items()))
            one_hot = np.zeros(94)
            one_hot[index] = 1
            img = cv2.imread(i)[..., ::-1]

            img = cv2.resize(img, (128, 256))
            x.append(img)
            y.append(one_hot)

        x =np.stack(x, axis=0)
        y = np.stack(y, axis=0)

        if aug:
            x = seq(images=x)

        yield x, y
