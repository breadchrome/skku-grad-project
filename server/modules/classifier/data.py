import numpy as np

from .util import *

import os
import pickle

from typing import Tuple, Iterable


def generate_dataset(data_path: str, window_size: int, slide_delta: int, tags: Iterable[str], prefix: str = None, ) -> Tuple[np.ndarray, np.ndarray]:
    """Load `*.npy` files and convert them to a format that can be feeded to the model.

    `*.npy` files are the results of `convert.py`.

    The filenames are expected to be in the format `{tag}.npy` if prefix is not specified or otherwise `{prefix}_{tag}.npy` for each tag.

    Args:
        data_path (str): The directory to load the files

        prefix (str): The prefixes of the input files

        window_size (int): The size of the window in number of sample

        slide_delta (int): The amount of displacement in number of samples between each consequtive windows

        tags(Iterable[str]): The list of labels

    Returns:
        Tuple[np.ndarray, np.ndarray]: Values and labels
    """
    prefix = "" if prefix is None else prefix + "_"
    values_parts = dict(
        (tag,
         slice_by_window(np.load(f'{data_path}/{prefix}{tag}.npy'), window_size, slide_delta),)
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

    return values, labels


def is_dataset_generated(data_path: str):
    """Test whether the directory contains preconverted dataset for training and testing.

    The directory specified by `data_path` must include two files: `dataset.train.pkl` and `dataset.test.pkl`

    Returns:
        bool: `True` if `data_path` contains the dataset or `False` otherwise
    """
    return os.path.isfile(f'{data_path}/dataset.train.pkl') and os.path.isfile(f'{data_path}/dataset.test.pkl')


def load_dataset(data_path: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Load preconverted dataset

    `is_dataset_generated(data_path)` must return `True` for the same `data_path` in order to work correctly

    Args:
        data_path (str): The directory to load the dataset from

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: `values_train`, `labels_train`, `values_test`, `labels_test`
    """
    with open(f'{data_path}/dataset.train.pkl', 'rb') as train_f, open(f'{data_path}/dataset.test.pkl', 'rb') as test_f:
        values_train, labels_train = pickle.load(train_f)
        values_test, labels_test = pickle.load(test_f)

    return values_train, labels_train, values_test, labels_test


def save_dataset(data_path: str, dataset: Tuple[np.ndarray, np.ndarray], portion: float = 0.9) -> None:
    """Split the values and labels from the dataset from `generate_dataset` to training and testing dataset and save the split data

    On successful execution, `is_dataset_generated(data_path)` will be satisfied.

    Args:
        data_path (str): The directory to save the dataset

        dataset (Tuple[np.ndarray, np.ndarray]): 2-element Tuple containing the values and labels

        portion (float): The ratio of the size of the training dataset to the entire dataset

    Returns:
        None
    """
    values, labels = dataset
    values_train, labels_train, values_test, labels_test =\
        split_data(values, labels, portion)

    with open(f'{data_path}/dataset.train.pkl', 'wb') as train_f, open(f'{data_path}/dataset.test.pkl', 'wb') as test_f:
        pickle.dump((values_train, labels_train), train_f)
        pickle.dump((values_test, labels_test), test_f)


if __name__ == "__main__":
    """Generate dataset"""
    # Load config
    config = load_config_from_argv()

    # Preprocess data
    dataset = generate_dataset(
        data_path=config["dirs"]["dataset"],
        **config["preprocessing"],  # window_size and slide_delta
        tags=config["tags"],
        prefix=config.get("prefix")
    )

    # Save preprocessed data
    save_dataset(config["dirs"]["dataset"], dataset)
