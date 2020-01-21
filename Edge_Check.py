"""
This script gives a visualized comparison between data
from the EdgeDetecion and the real image. Just change
the file name below and run the code. It assumes the 
tip of icicle is pointing downward in the image. The
code is tested in Jupyter Notebook. 
"""

# Note: '.png' or '.jpg' extension is required
fileName = 'Icicle_test.jpg'


#######################################################


import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
import imageio as io
from Edge_Detect import EdgeDetect


# Get edge data
left, right = EdgeDetect(fileName)

x = np.arange(0,len(left))

# Read the image and rotate by 90 degree
img = io.imread(fileName)
tr = ndimage.rotate(img,90)

# Flip the image upside down
tr_ud = np.flipud(tr)

# Use the sizes of the image as dimensions of the figure
x_size, y_size, channel = img.shape
fig, ax = plt.subplots(figsize=(x_size/100, y_size/100))

# Show the image
ax.imshow(tr_ud, origin='lower')

# Plot the data
plt.plot(x, right)
plt.plot(x, left)
plt.show()
