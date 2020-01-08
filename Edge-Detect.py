#!/usr/bin/env python
# coding: utf-8

# In[23]:


# Icicle Edge Detection Script
# Using OpenCV, find left and right edges of the icicle.
# Performed using OpenCV thresholding then analyzing difference in brightness values of threshold.

import cv2 as cv
import sys
import numpy as np


def EdgeDetect(imageloc,threshold=110,kernalsize=3,lbound=100,ubound=200):

    k=kernalsize
    
    try:
        img = cv.imread(filename = imageloc,flags = cv.IMREAD_GRAYSCALE)
    except:
        return str("No compatible image found at ",imageloc)
    
    blurred = cv.GaussianBlur(src = img, ksize = (k, k), sigmaX = 0.1)
    
    (t, mask) = cv.threshold(src = blurred, thresh = threshold, maxval = 255,type = cv.THRESH_BINARY)

    edges = cv.Canny(mask,lbound,ubound)
    
    leftedge = list(np.zeros(len(edges)))
    rightedge = list(np.zeros(len(edges)))
    
    missedpix = 0
    endpix = 0
    
    for i in range(0,len(edges)):
        if missedpix < 2:
            try:
                edgedetection = np.nonzero(edges[i])[0]
                leftedge[i] = edgedetection[0]
                rightedge[i]= edgedetection[-1]
            except:
                missedpix += 1
                endpix = i
            
    del leftedge[endpix-1:]
    del rightedge[endpix-1:]
        
    return leftedge,rightedge

