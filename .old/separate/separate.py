#/usr/bin/python3

import sys
import os
from math import sin, cos, pi

with open(sys.argv[1]) as csi_file:
    csv = [row.split(",") for row in csi_file.readlines()]
    csv_path = csi_file.name

n_antennas = len(csv[0]) // 60
timestamps = [float(row[0]) for row in csv]
t_range = timestamps[-1] - timestamps[0]
t_min = timestamps[0]
timestamps = [(t - t_min) for t in timestamps]
subcarriers_rows = [[float(col) for col in row] for row in (row[1:] for row in csv)]

out = [ [[] for _ in range(30)] ] * n_antennas
i = 0
for subcarriers in subcarriers_rows:
    for antenna in range(n_antennas):
        amplitudes, phases = subcarriers[60*antenna:60*antenna+30], subcarriers[60*antenna+30:60*(antenna+1)]
        for subcarrier, (amplitude, phase,) in enumerate(zip(amplitudes, phases)):
            out[antenna][subcarrier].append((amplitude, phase,))

os.mkdir(f"{csv_path}.scs")

for n_antenna, antenna in enumerate(out):
    for n_subcarrier, subcarrier in enumerate(antenna):
        with open(f"{csv_path}.scs/a{n_antenna}.s{n_subcarrier}.csv", "w") as outfile:
            for timestamp, (amp, phs,) in zip(timestamps, subcarrier):
                phs /= 2 * pi
                outfile.write(f"{timestamp},{amp * cos(phs)},{amp * sin(phs)}\n")