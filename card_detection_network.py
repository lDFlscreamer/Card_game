import os
from datetime import datetime

import tensorflow as tf
from keras.callbacks import ModelCheckpoint
from tensorflow.keras.layers import *
from tensorflow.keras.models import *

import CONSTANT
import dataset_handler

STEPS_PER_EPOCH = 25
VALIDATION_STEPS_PER_EPOCH = int(STEPS_PER_EPOCH / 10) + 1
EPOCH_NUMBER = 2000
TRAIN_BATCH_SIZE = 32
TEST_BATCH_SIZE = 8

# learning rate schedule
INITIAL_LR = 1e-1
DECAY_RATE = 0.5

# EarlyStopping
EARLY_STOPPING_MIN_DELTA = 0
EARLY_STOPPING_PATIENCE = 100
EARLY_STOPPING_BASELINE = 0.8


def get_conv_model(dim=CONSTANT.INPUT_IMAGE_SHAPE, out=CONSTANT.OUTPUT_SHAPE, dropout=0.6):
    inp_shape = dim
    drop = dropout

    model = Sequential()
    model.add(Conv2D(filters=8, kernel_size=(3, 3), padding="valid",
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


def get_model(out=CONSTANT.OUTPUT_SHAPE, use_new=False):
    model_is_exist = os.path.exists(CONSTANT.DETECTION_MODEL_PATH)
    if use_new or (not model_is_exist):
        return get_conv_model(dim=CONSTANT.INPUT_IMAGE_SHAPE, out=out)
    if model_is_exist:
        return load_model(CONSTANT.DETECTION_MODEL_PATH)


def get_callbacks():
    log_dir = CONSTANT.TENSORBOARD_LOG_DIR + datetime.now().strftime("%Y%m%d-%H-%M-%S")
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
    loss_checkpoint = ModelCheckpoint(CONSTANT.DETECTION_MODEL_PATH, monitor='accuracy', verbose=1,
                                      save_best_only=True, mode='auto', save_freq='epoch')
    accuracy_checkpoint = ModelCheckpoint(CONSTANT.DETECTION_ACCURACY_MODEL_PATH,
                                          monitor='val_accuracy',
                                          verbose=1,
                                          save_best_only=True, mode='auto', period=1)
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor="val_accuracy",
                                                      min_delta=EARLY_STOPPING_MIN_DELTA,
                                                      patience=EARLY_STOPPING_PATIENCE,
                                                      verbose=1,
                                                      mode="auto",
                                                      baseline=EARLY_STOPPING_BASELINE,
                                                      restore_best_weights=False,
                                                      )
    return [
        tensorboard_callback,
        loss_checkpoint,
        accuracy_checkpoint,
        early_stopping
    ]


def get_lr_schedule(init_lr=INITIAL_LR, decay_rate=DECAY_RATE):
    lr_schedule = tf.keras.optimizers.schedules.InverseTimeDecay(
        initial_learning_rate=init_lr,
        decay_steps=STEPS_PER_EPOCH * 1000,
        decay_rate=decay_rate,
        staircase=False)
    return lr_schedule


def learn_model(model, train_gen, test_gen, verbose=True):
    optimizer = tf.keras.optimizers.Adam(learning_rate=get_lr_schedule())
    model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

    fit_verbose = 2
    if verbose:
        model.summary()
        fit_verbose = 1

    model.fit(
        train_gen,
        steps_per_epoch=STEPS_PER_EPOCH,
        epochs=EPOCH_NUMBER,
        validation_data=test_gen,
        validation_steps=VALIDATION_STEPS_PER_EPOCH,
        verbose=fit_verbose,
        callbacks=get_callbacks()
    )


def get_card_detection(with_aug=False):
    model_is_exist = os.path.exists(CONSTANT.DETECTION_ACCURACY_MODEL_PATH)
    if not model_is_exist:
        data, data_len = dataset_handler.get_data()
        train_gen = dataset_handler.data_gen(batch_size=TRAIN_BATCH_SIZE, aug=with_aug)
        test_gen = dataset_handler.data_gen(batch_size=TEST_BATCH_SIZE, aug=False)
        model = get_model(out=data_len + 1)
        learn_model(model, train_gen, test_gen)
    return load_model(CONSTANT.DETECTION_ACCURACY_MODEL_PATH)
