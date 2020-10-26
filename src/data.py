import numpy as np
import sys
import pickle
import config
import os

from typing import Tuple
from util import *


def slice_by_window(record: np.ndarray, window_size: int = config.WINDOW_LENGTH, slide_delta: int = config.SLIDE_DELTA) -> np.ndarray:
    n_packets, _ = record.shape
    slices = tuple(
        record[i:i+window_size, ...]
        for i in range(0, n_packets - window_size, slide_delta)
    )

    return np.stack(slices)


def convert_data(data_path, prefix="", window_size: int = config.WINDOW_LENGTH, slide_delta: int = config.SLIDE_DELTA, tags = config.TAGS) -> Tuple[np.ndarray, np.ndarray]:
    if prefix:
        prefix += "_"
    values_parts = dict(
        (tag, slice_by_window(
            np.load(f'{data_path}/{prefix}{tag}.npy'), window_size, slide_delta),)
        for tag in tags
    )

    values = np.concatenate(
        tuple(values_parts.values()), axis=0)
    labels = np.concatenate(
        tuple(
            np.tile(
                np.array([1 if tags[i] == tag else 0 for i in range(len(tags))]),
                (values_parts[tag].shape[0], 1)
            )
            for tag in values_parts.keys()
        )
    )

    return shuffle_arrays(values, labels)

def is_data_converted(data_path):
    return os.path.isfile(f'{data_path}/dataset.train.pkl') and os.path.isfile(f'{data_path}/dataset.test.pkl')

def load_data(data_path):
    with open(f'{data_path}/dataset.train.pkl', 'rb') as train_f, open(f'{data_path}/dataset.test.pkl', 'rb') as test_f:
        values_train, labels_train = pickle.load(train_f)
        values_test, labels_test = pickle.load(test_f)

    return values_train, labels_train, values_test, labels_test

def save_data(data_path, dataset, portion=0.9):
    values, labels = dataset
    values_train, labels_train, values_test, labels_test = split_data(values, labels, portion)

    with open(f'{data_path}/dataset.train.pkl', 'wb') as train_f, open(f'{data_path}/dataset.test.pkl', 'wb') as test_f:
        pickle.dump((values_train, labels_train), train_f)
        pickle.dump((values_test, labels_test), test_f)


if __name__ == "__main__":
    values, labels = convert_data(sys.argv[1])

    save_data(sys.argv[1], (values, labels))