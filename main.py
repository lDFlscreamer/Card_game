# from matplotlib import pyplot as plt
#
# from card_detection import dataset_handler
#
# sample_image = dataset_handler.prepare_img('card_detection/dataset/card/101.jpg')
# plt.imshow(sample_image)
# plt.show()
import numpy as np
from numpy import unravel_index

rand = np.random.randint(low=0, high=95, size=(94, 94,94))

axis = np.max(rand)
axis = unravel_index(rand.argmax(), rand.shape)
print(axis)
