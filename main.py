import matplotlib.pyplot as plt
import numpy as np
from keras.models import load_model

import dataset_aug as dataset_gen

# model = load_model('models/detection_model.h5')
#
# # получить прогноз для этого изображения
dataset = dataset_gen.data_gen(batch_size=128, aug=True)
#
data_sample = next(dataset)
sample_image = data_sample[0][0]
# sample_label = data_sample[1][0]
# prediction = np.argmax(model.predict(sample_image))
plt.imshow(sample_image)
# print("Predicted label:", prediction)
# print("True label:", sample_label)
