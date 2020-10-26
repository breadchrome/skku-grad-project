import sys
import keras
import numpy as np

from sklearn.model_selection import KFold

from model import ModelConfig
from data import *
from util import *

import config

import sys, os

if __name__ == "__main__":
    if not is_data_converted(sys.argv[1]):
        dataset = convert_data(sys.argv[1])
        save_data(sys.argv[1], dataset)

    x_train, y_train, x_test, y_test = load_data(sys.argv[1])

    if not os.path.exists(sys.argv[2]):
        os.mkdir(sys.argv[2])

    skf = KFold(n_splits=5, shuffle=True)
    for idx, (train, valid) in enumerate(skf.split(x_train, y_train)):
        x_train_ = x_train[train]
        y_train_ = y_train[train]
        x_valid_ = x_train[valid]
        y_valid_ = y_train[valid]

        model = ModelConfig.build_model()
        model.summary()

        callback = keras.callbacks.ModelCheckpoint(
            f'{sys.argv[2]}/model_{idx}.h5',
            monitor='val_loss',
            mode='min',
            verbose=1,
            save_best_only=True)
        model.fit(x_train_, y_train_,
            batch_size=config.TRAIN_BATCH_SIZE, 
            epochs=config.TRAIN_EPOCHS, 
            validation_data=(x_valid_, y_valid_),
            callbacks=[callback])
        model.load_weights(f'{sys.argv[2]}/model_{idx}.h5')

        print(model.evaluate(x_valid_, y_valid_))
