#!/usr/bin/env python
# coding: utf-8

# In[ ]:


'''
ELSA Icicle Spine Analyzer designed to center left and right bounds of icicle to zero for fitting to response function.
In addition, if the icicle is curved, this script will use a linear fit to renormalize the edges first.
There are two functions in this script, SpineCalc and SpineCorrection, with the latter being used in the former.
Use help(SpineCalc) for more information.
'''
#Import numpy
import numpy as np

def SpineCorrection(left,right,spine):
'''
Correction function for curved icicles processed by SpineCalc. This function will run automatically if required,
set by the threshold parameter in the SpineCalc function.
'''
    #Set up linear space to perform the linear fit over
    zspace = np.linspace(0,len(spine),len(spine))
    
    #Calculate linear fit for icicle spine
    scoliosis = np.polyfit(zspace,spine,1)
    
    #Calculate corrected left and right edges
    leftcorr = left-scoliosis[zspace]
    rightcorr = right-scoliosis[zspace]
    
    return leftcorr,rightcorr

def SpineCalc(left,right,threshold=5):
'''
ELSA edge adjustment function to center the left and right edges around the spine of the icicle. If needed, this
function will also renormalize these edges to a linear fit if the icicle is curved. Takes the following arguments:

left as list: Position array of the left edge of the icicle.
right as list: Position array of the right edge of the icicle.
threshold as int: Maximum distance that any point on the icicle spine can be from the average of the spine.

And returns the following:

leftfin as list: Final renormalized list for positions of the left edge of the icicle.
rightfin as list: Final renormalized list for positions of the right edge of the icicle.
'''
    #Calculate the spine of the icicle and its mean value.
    spine = (right+left)/2
    mean = np.mean(spine)
    
    #Check if the spine of the icicle differs from its mean by more than the threshold
    if max(abs(spine-mean)) > threshold:
        
        #If so, prepare left and right arrays around zero, then run correction script
        leftuncorr = mean-left
        rightuncorr = right-mean
        leftfin, rightfin = SpineCorrection(leftuncorr,rightuncorr,spine)
    else:
        
        #If not, just return the edges normalized around zero
        leftfin = mean-left
        rightfin = right-mean
        
    return leftfin,rightfin

