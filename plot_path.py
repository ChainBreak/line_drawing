#!/usr/bin/env python3

import argparse
import math
from matplotlib import pyplot as plt

def plot(path_list):
    count = 0
    for path in path_list:
        x,y = zip(*path)
        y = [-v for v in y]
        plt.plot(x,y,"-k")
        # plt.plot(x,y,"+r")

        count += len(y)

    print("count",count)
    plt.show()
