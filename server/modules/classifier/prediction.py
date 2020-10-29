import numpy as np

from .util import slice_by_window
from .model import ModelConfig

import logging

from typing import List


class Predictor:
    def __init__(self, model_config: dict, model_weights_path: str, tick: int) -> None:
        self.window_delta = tick // 2
        self.model_config = dict(**model_config)
        self.model = ModelConfig.build_model(**model_config)
        self.model.load_weights(model_weights_path)

    def load_and_predict(self, csi_data_path: str) -> np.ndarray:
        logging.getLogger().debug("Loading CSI npy file")
        x = np.load(csi_data_path)
        logging.getLogger().debug("Loaded CSI npy file")
        return self.predict(x)

    def predict(self, csi_data: np.ndarray) -> np.ndarray:
        logging.getLogger().debug("Slicing CSI data")
        x = slice_by_window(csi_data, self.model_config["window_length"], self.window_delta)
        logging.getLogger().debug("Slicing complete. Generating prediction...")
        y = np.argmax(self.model.predict(x), axis=1)
        logging.getLogger().debug("Prediction complete...")
        return y


if __name__ == "__main__":
    # _, npy_path = sys.argv
    model_config = {
        "tags": 5,
        "window_length": 1000,
        "input_size": 30,
        "units_lstm": 200,
        "learning_rate": 1e-5
    }
    weights = "classifier/saved_model/without_phase/model_1.h5"
    predictor = Predictor(model_config, weights)

    y = predictor.load_and_predict(
        "../../data/csi/without_phase/virtual_sleep.npy")

    print(np.bincount(y))
    print(y)
