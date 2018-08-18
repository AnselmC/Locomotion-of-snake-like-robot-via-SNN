import math

import numpy as np
import matplotlib.pylab as plt
import pandas as pd

height = 3.0
height_strip = 0.25
delta_height = height - 2*height_strip
width = 2.5
width_wall = 0.2

bottom_1 = [0.,             width,
            height_strip,   width,
            height_strip,   width + width_wall,
            0.,             width + width_wall]
bottom_1 = np.array(bottom_1)

bottom_2 = [0.,             -width,
            height_strip,   -width,
            height_strip,   -width - width_wall,
            0.,             -width - width_wall]
bottom_2 = np.array(bottom_2)

delta_middle = [height_strip, 0,
                delta_height, 0,
                delta_height, 0,
                height_strip, 0,]
delta_middle = np.array(delta_middle)

middle_1 = bottom_1 + delta_middle
middle_2 = bottom_2 + delta_middle

delta_top = [delta_height, 0,
             height_strip, 0,
             height_strip, 0,
             delta_height, 0]

top_1 = middle_1 + delta_top
top_2 = middle_2 + delta_top

data = [bottom_1,
        bottom_2,
        middle_1,
        middle_2,
        top_1,
        top_2]

df = pd.DataFrame(data=data)

df.to_csv(path_or_buf="vrep-path-shape.csv",
          header=False,
          index=False)
