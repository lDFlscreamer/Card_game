from matplotlib import pyplot as plt

import dataset_handler

sample_image = dataset_handler.prepare_img('dataset/card/101.jpg')
plt.imshow(sample_image)
plt.show()
