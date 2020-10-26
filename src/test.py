from data import convert_data
from model import *
from data import *
from util import *
from sklearn.metrics import confusion_matrix

import sys
import glob

if __name__ == "__main__":
    model = ModelConfig.build_model()
    
    for filename in glob.glob(f'{sys.argv[2]}/model_*.h5'):
        model.load_weights(filename)

        x_test, y_test = convert_data(sys.argv[1], prefix='test')
        y_pred = model.predict(x_test)

        print(confusion_matrix(np.argmax(y_test, axis=1), np.argmax(y_pred, axis=1)))