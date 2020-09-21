#!/usr/bin/env bash

sudo ~/csi/linux-80211n-csitool-supplementary/netlink/log_to_file ~/csi/project/data/ours/$1.dat
octave ~/csi/project/src/convert/convert.m ~/csi/project/data/ours/$1.dat ~/csi/project/data/ours/$1.csv
python ~/csi/project/src/separate/separate.py ~/csi/project/data/ours/$1.csv