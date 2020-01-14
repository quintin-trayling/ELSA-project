'''
ELSA Icicle Edge Detection Script designed to find the left and right edges of the icicle using OpenCV.
Performed using OpenCV thresholding then analyzing difference in brightness values of threshold.
There is only one function in this script, EdgeDetect. Use help(EdgeDetect) for more details.
'''
#Import required libraries
import cv2 as cv
import sys
import numpy as np


def EdgeDetect(imageloc,threshold=110,kernalsize=3,bound=20):
    '''
    ELSA Edge Detection Function. Takes the following arguments:

    imageloc as string: relative path to the icicle image for processing.
    threshold as int: Brightness threshold for OpenCV Thresholding. Defaults to 110.
    kernalsize as int: Kernal Size for OpenCV Blurring. Defaults to 3.
    bound as int: Upper and lower bounds for edge detection (relative to threshold) using OpenCV Canny. Defaults to 20.
    And returns the following:

    leftedge as list: Pixel locations for left icicle edge, from base to tip
    rightedge as list: Pixel locations for right icicle edge, from base to tip
    '''
    #Contract kernal size variable for ease of use
    k=kernalsize
    
    #Calculate lbound and ubound using threshold and bound.
    lbound = max(0,threshold-bound)
    ubound = min(255,threshold+bound)
    
    #Try reading the image file, returning an error if read fails
    try:
        img = cv.imread(filename = imageloc,flags = cv.IMREAD_GRAYSCALE)
    except:
        return str("No compatible image found at ",imageloc)
    
    #Gaussian Blur the icicle image
    blurred = cv.GaussianBlur(src = img, ksize = (k, k), sigmaX = 0.1)
    
    #Brightness threshold the blurred image to calculate outside edges.
    (t, mask) = cv.threshold(src = blurred, thresh = threshold, maxval = 255,type = cv.THRESH_BINARY)
    edges = cv.Canny(mask,lbound,ubound)
    
    #Initialize arrays for optimal memory usage.
    leftedge = list(np.zeros(len(edges)))
    rightedge = list(np.zeros(len(edges)))
    
    #Create ints for missed pixels (pixels where no edges can be found) and the ending pixel of the icicle.
    missedpix = 0
    endpix = 0
    
    #Iterate over the height of the image
    for i in range(0,len(edges)):
        
        #Check if 2 or more pixels have been missed
        if missedpix < 2:
            #If not, try to find the next edge, and save the pixels to the arrays
            try:
                edgedetection = np.nonzero(edges[i])[0]
                leftedge[i] = edgedetection[0]
                rightedge[i]= edgedetection[-1]
            #If fails, consider this a "missed" pixel
            except:
                missedpix += 1
                endpix = i
        #If 2 or more pixels have been missed, then stop iterating, since this is likely the end of the icicle.
        else:
            break
            
    #Remove array elements beyond the end of the icicle so the image can be easily reversed
    del leftedge[endpix-1:]
    del rightedge[endpix-1:]
        
    #Return the calculated edges
    return leftedge,rightedge
