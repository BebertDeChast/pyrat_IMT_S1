import matplotlib.pyplot as plt
import numpy as np


filename = "PyRat-1-master/saves/1665990486409"
with open(filename) as f:
    lastline = f.readlines()[-1]
    print(lastline)
    d = eval(lastline)
    print(d["moves_rat"])
