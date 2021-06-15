import numpy as np
from matplotlib import pyplot as plt

import card_detection_network as c_d
import dataset_handler


def detect_card(imaged_paths: []):
    network = c_d.get_card_detection()
    imgs_to_predict = dataset_handler.prepare_imgs(imaged_paths)
    predictions = network.predict(np.vstack(imgs_to_predict))
    argmax_predictions = np.argmax(predictions, axis=1)
    return [dataset_handler.get_label(x) for x in argmax_predictions]


def test_detection():
    # prepare data
    dataset = dataset_handler.data_gen(batch_size=1, aug=False)
    data_sample = next(dataset)

    sample_image = data_sample[0]
    sample_label = data_sample[1]

    # do a prediction
    network = c_d.get_card_detection()
    prediction = network.predict(sample_image)
    # show card
    plt.imshow(sample_image[0])
    plt.show()

    # output prediction
    # predicted
    print("Predicted label:", prediction[0])
    argmax_prediction = np.argmax(prediction[0])
    print("Predicted label:", argmax_prediction)
    print("Predicted label:", dataset_handler.get_label(argmax_prediction))
    # true label
    argmax_true = np.argmax(sample_label[0])
    print("True label:", sample_label[0])
    print("True label:", argmax_true)
    print("True label:", dataset_handler.get_label(argmax_true))


test_detection()
