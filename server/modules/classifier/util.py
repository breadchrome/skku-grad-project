import numpy as np

import sys
import json


def slice_by_window(record: np.ndarray, window_size: int, slide_delta: int) -> np.ndarray:
    """Slice the n-dimensional array along the first axis by a sliding window

    Args:
        record (np.ndarray): An n-dimensional array to apply the sliding window

        window_size (int): Size of the window

        slide_delta (int): The amount of displacement in number of samples between each consequtive windows
    """
    n_packets, _ = record.shape
    slices = tuple(
        record[i:i+window_size, ...]
        for i in range(0, n_packets - window_size, slide_delta)
    )

    return np.stack(slices)


def split_data(*args: np.ndarray, portion=0.8):
    split_idxs = (int(portion * len(arg)) for arg in args)
    split_pairs = ((arr[:i, ...], arr[i:, ...])
                   for (arr, i) in zip(args, split_idxs))
    l_parts, r_parts = zip(*split_pairs)
    return tuple((*l_parts, *r_parts))


def shuffle_arrays(*args, axis=0):
    permutation = np.arange(args[0].shape[axis])
    np.random.shuffle(permutation)
    for arg in args:
        print(arg.shape)
    return (arg[permutation] for arg in args)


def load_config_from_argv(exit_on_error: bool = True) -> dict:
    try:
        try:
            _, config_path = sys.argv
        except Exception as e:
            print(f"Usage: python3 {sys.argv[0]} {{config_path}}")
            raise e
        try:
            with open(config_path) as config_file:
                config = json.load(config_file)
                return config
        except Exception as e:
            print(f"Failed to open config file: {config_path}")
            raise e
    except Exception as e:
        if exit_on_error:
            sys.exit(1)
        else:
            raise e
