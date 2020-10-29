import csiread
import numpy as np
import scipy.signal as sp
import sys
import glob

import config

if __name__ == "__main__":
    """
    Converts binary csi data into NumPy matrices.

    If phase is enabled, each row has 60 columns (30 subcarriers) * (amplitude, phase)
    If not, each row has 30 columns.
    """

    _, dir, mode = sys.argv

    input = None
    for filename in glob.glob(f'{dir}/*_{mode}.dat'):
        csi = csiread.CSI(filename, Ntxnum=1)
        csi.read()
        scaled_csi = np.sum(csi.get_scaled_csi().squeeze(-1), axis=2)

        amplitude = np.abs(scaled_csi)
        phase = np.angle(scaled_csi)

        cur_input = np.concatenate((amplitude, phase), axis=1) if config.USE_PHASE else amplitude
        input = np.concatenate((input, cur_input), axis=0) if input is not None else cur_input

    print(input.shape)
    np.save(f'{dir}/{mode}.npy', input, False)
