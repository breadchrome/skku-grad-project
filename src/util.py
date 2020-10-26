import numpy as np

def split_data(x, y, portion=0.8):
    x_train, x_valid = x[:int(portion * len(x)),...], x[int(portion * len(x)):, ...]
    y_train, y_valid = y[:int(portion * len(y)),...], y[int(portion * len(y)):, ...]

    return x_train, y_train, x_valid, y_valid

def shuffle_arrays(*args, axis=0):
    permutation = np.arange(args[0].shape[axis])
    np.random.shuffle(permutation)
    return (arg[permutation] for arg in args)