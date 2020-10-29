import keras
from sklearn.model_selection import KFold
import numpy as np

from .data import *
from .model import ModelConfig
from .util import *

import os

if __name__ == "__main__":
    # Load config
    config = load_config_from_argv()

    # Convert and save if dataset is not already converted
    if not is_dataset_generated(config["dirs"]["dataset"]):
        dataset = generate_dataset(
            config["dirs"]["dataset"],
            config["model"]["window_size"],
            config["model"]["slide_delta"],
            config["tags"]
        )
        save_dataset(config["dirs"]["dataset"], dataset)

    # Load dataset
    x_train, y_train, x_test, y_test = load_dataset(config["dirs"]["dataset"])
    x_train, y_train = shuffle_arrays(x_train, y_train)
    x_test, y_test = shuffle_arrays(x_test, y_test)

    # Create directory to store the model
    if not os.path.exists(config["dirs"]["model"]):
        os.mkdir(config["dirs"]["model"])

    # Perform k-fold cross validation
    skf = KFold(n_splits=5, shuffle=True)
    for idx, (train, valid) in enumerate(skf.split(x_train, y_train)):
        # Load training and validation data
        x_train_ = x_train[train]
        y_train_ = y_train[train]
        x_valid_ = x_train[valid]
        y_valid_ = y_train[valid]

        # Build model and print summary
        model = ModelConfig.build_model(**config["model"])
        model.summary()

        # Train model
        callback = keras.callbacks.ModelCheckpoint(
            f'{config["dirs"]["model"]}/model_{idx}.h5',
            monitor='val_loss',
            mode='min',
            verbose=1,
            save_best_only=True,
        )
        model.fit(
            x_train_, y_train_,
            **config["training"],
            validation_data=(x_valid_, y_valid_),
            callbacks=[callback],
        )

        # Test run final model
        model.load_weights(f'{config["dirs"]["model"]}/model_{idx}.h5')
        print(model.evaluate(x_valid_, y_valid_))
