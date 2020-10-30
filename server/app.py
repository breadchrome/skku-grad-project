from flask import Flask
from flask_cors import CORS
from flask import request

from modules.classifier.prediction import Predictor

import json
import logging

from datetime import datetime
import sys

CONFIG_PATH = "config/nophase.json"

with open(CONFIG_PATH) as config_f:
    config = json.load(config_f)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))

logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

predictor = Predictor(
    config["model"],
    f"{config['dirs']['model']}/{config['prod']['model']}",
    config["prod"]["tick"]
)

logging.getLogger().info("Predictor initialized")

@app.route('/sleeping-analysis')
def sleeping_analysis():
    max_timeline_len = request.args.get('max_timeline_len', default=100, type=int)
    user = request.args.get('user', default='test')
    date = request.args.get('date')

    timeline_ndarray = predictor.load_and_predict("data/sleep/20201029.npy")
    timeline_len = len(timeline_ndarray)

    stride = timeline_len // max_timeline_len

    return {
        'tick': config["prod"]["tick"] * stride,
        'start': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'tags': config["tags"],
        'timeline': timeline_ndarray[::stride].tolist()
    }

logging.getLogger().info("Init complete")