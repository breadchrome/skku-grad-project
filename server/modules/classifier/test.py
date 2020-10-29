from .model import *
from .data import *
from .util import *
from sklearn.metrics import confusion_matrix

import sys
import glob
import json


if __name__ == "__main__":
    # Load config
    try:
        _, config_dir = sys.argv
    except:
        print(f"Usage: python3 {sys.argv[0]} {{config_dir}}")
        sys.exit(1)
    with open(sys.argv[1]) as config_file:
        config = json.load(config_file)

    model = ModelConfig.build_model(**config["model"])

    for filename in glob.glob(f'{config["dirs"]["model"]}/model_*.h5'):
        model.load_weights(filename)

        x_test, y_test = generate_dataset(
            data_path=config["dirs"]["dataset"],
            **config["preprocessing"],  # window_size and slide_delta
            tags=config["tags"],
            prefix="test"
        )
        y_pred = model.predict(x_test)

        print(filename)
        print(confusion_matrix(np.argmax(y_test, axis=1), np.argmax(y_pred, axis=1)))
