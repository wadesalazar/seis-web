import segyio
import numpy as np
import json

f = segyio.open('C:\\Users\\wades\\workspace\\segy\\CSDS28_1.SGY', ignore_geometry = True)

sample = np.random.choice(f.trace[0], 20)

def xyEncode(data):
    a = []
    i = 0
    offset = 10
    threshold = 3000
    width = threshold / offset
    for x in data:
        if x > threshold or x < -(threshold):
            x2 = 0
        else:
            x2 = x
        x2 = x2 / width
        y = offset+(offset * i)
        a.append({"x": x2,"y": y})
    i += 1

    return a

print(xyEncode(sample))

