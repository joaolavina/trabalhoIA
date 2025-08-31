import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from heapq import heappush, heappop

grid = [
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 3, 1, 1, 1, 1],
    [1, 1, 2, 2, 1, 3, 3, 2, 1, 1],
    [1, 1, 2, 1, 3, 3, 3, 2, 1, 1],
    [1, 1, 2, 2, 3, 3, 3, 2, 2, 1],
    [1, 1, 1, 2, 3, 1, 2, 2, 1, 1],
    [1, 1, 1, 1, 2, 3, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1]
]
