import os
from datetime import datetime

import tensorflow as tf
from keras.callbacks import ModelCheckpoint
from tensorflow.keras.layers import *
from tensorflow.keras.models import *

import dataset_aug as dataset_gen

STEPS_PER_EPOCH = 25


def get_model(dim=(256, 128, 3), out=94, use_new=False):
    model_is_exist = os.path.exists("%sdetection_model.h5" % card_detection_folder)
    if use_new or (not model_is_exist):
        return get_conv_model(dim=dim, out=out)
    if model_is_exist:
        return load_model("%sdetection_model.h5" % card_detection_folder)


def get_conv_model(dim=(256, 128, 3), out=94):
    inp_shape = dim
    drop = .25

    model = Sequential()
    model.add(Conv2D(filters= 8, kernel_size=(3, 3), padding="valid",
                     input_shape=inp_shape, activation="relu"))

    model.add(Dropout(drop))

    model.add(Conv2D(filters=8, kernel_size=(3, 3), padding="valid", activation="relu"))

    model.add(Conv2D(filters=8, kernel_size=(3, 3), padding="valid", activation="relu"))

    model.add(Conv2D(filters=8, kernel_size=(3, 3), padding="valid", activation="relu"))

    model.add(Dropout(drop))

    model.add(Conv2D(filters=32, kernel_size=(3, 3), padding="valid", activation="relu"))

    model.add(Conv2D(filters=32, kernel_size=(3, 3), padding="valid", activation="relu"))

    model.add(Conv2D(filters=32, kernel_size=(3, 3), padding="valid", activation="relu"))

    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(filters=64, kernel_size=(3, 3), padding="valid", activation="relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(filters=64, kernel_size=(3, 3), padding="valid", activation="relu"))

    model.add(Conv2D(filters=32, kernel_size=(3, 3), padding="valid", activation="relu"))

    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(filters=16, kernel_size=(3, 3), padding="valid", activation="relu"))

    model.add(Conv2D(filters=8, kernel_size=(3, 3), padding="valid", activation="relu"))

    model.add(Conv2D(filters=4, kernel_size=(3, 3), padding="valid", activation="relu"))

    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(drop))

    model.add(Flatten())
    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(drop))
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(drop))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(drop))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(drop))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(drop))
    model.add(Dense(out, activation="softmax"))
    return model


data, data_len = dataset_gen.get_data()
train_gen = dataset_gen.data_gen(batch_size=32, aug=False)
test_gen = dataset_gen.data_gen(batch_size=8, aug=False)
# tensorboard
log_dir = "logs/fit/" + datetime.now().strftime("%Y%m%d-%H-%M-%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
card_detection_folder = "models/cardDetection/"
checkpoint = ModelCheckpoint("%sdetection_model.h5" % card_detection_folder, monitor='loss', verbose=1,
                             save_best_only=True, mode='auto', period=1)
checkpoint1 = ModelCheckpoint("%sdetection_model_accuracy.h5" % card_detection_folder, monitor='val_accuracy',
                              verbose=1,
                              save_best_only=True, mode='auto', period=1)

lr_schedule = tf.keras.optimizers.schedules.InverseTimeDecay(
    1e-3,
    decay_steps=STEPS_PER_EPOCH * 1000,
    decay_rate=1,
    staircase=False)

optimizer = tf.keras.optimizers.Adam(learning_rate=lr_schedule)

model = get_model(dim=(256, 128, 3), out=data_len + 1)
model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
model.summary()
#
model.fit(
    train_gen,
    steps_per_epoch=STEPS_PER_EPOCH,
    epochs=1000,
    validation_data=test_gen,
    validation_steps=int(STEPS_PER_EPOCH / 10) + 1,
    verbose=1,
    callbacks=[checkpoint,
               tensorboard_callback,
               checkpoint1
               ]
)
