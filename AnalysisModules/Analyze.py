'''
ELSA Main Analysis script for finding fit parameters of icicle edges.
This script only has one function, Analyze, which will perform the Edge Detection, Spine Correction, and Edge Fitting
of the left and right sides of the icicle. Use help(Analyze) for more information.
'''

#Main Icicle Analysis Script. Combines functionality of all previous scripts into one convenient location.
#Import required libraries
import numpy as np
import matplotlib.pyplot as plt

from .Edge_Detect import EdgeDetect
from .Spine_Analyzer import SpineCalc
from .Edge_Fit import EdgeFit

def Analyze(imageloc,ppcm=95,edgethreshold=110,kernalsize=3,detectionbound=20,spinethreshold=5,
            parguess=[],error=0,sigma_abs = True,amplitudethresh=0.01,amplituderes=3,amplitudeiter=4,
           ignoreIterate = False,oscillationFit = True):
    '''
    Main analysis function for ELSA edge detection and fitting. Combines functionality of Edge_Detect, Spine_Analyzer, and
    Edge_Fit to quickly return icicle fit parameters and uncertainties. Takes the following arguments:

    imageloc as string: Relative location of icicle image file.
    ppcm as int: Pixels per centimeter in camera image. Defaults to 95 (original estimate from ELSA TDR)
    kernalsize as int: Kernal size for icicle edge detection. Defaults to 3.
    detectionbound as int: Icicle edge detection threshold using openCV Canny. Defaults to 20.
    spinethreshold as int: Threshold for how far away from the mean is considered to require Spine Correction. Defaults to 5.
    parguess as array: guess values for parameters, as follows, from section 2.3 of ELSA TDR: [A_r,w,phi,C_r]. Defaults to [A_guess,w_guess,0,C_guess], where A_guess, w_guess, and C_guess are calculated by the AmplitudeGuess, FrequencyGuess, and OffsetGuess functions, respectively.
    error as array-like: Error on response values. Defaults to max(response)/(len(response))**(1/2)
    sigma_abs as Boolean: Whether or not to use absolute_sigma in curve_fit. Defaults to True.
    bounds as 2 arrays: Lower and upper bounds on fit parameters
    amplitudethresh as float: Thresholding value for AmplitudeGuess function. Defaults to 0.01.
    amplituderes as int: Resolution value for AmplitudeGuess Function. Defaults to 3.
    amplitudeiter as int: Number of iterations to average over for the AmplitudeGuess function. Defaults to 4.
    ignoreIterate as boolean: Whether to continue iteration of amplitude guesses after the fixed number of iterations given in amplitudeiterations. Defaults to False.
    oscillationFit as boolean: Whether to perform a fit on the icicle oscillations rather than just returning the parameter guesses. Defaults to True.
    
    And returns the following:

    Note that the output arrays output data in the following format:
    out = [A_r,w_r,phi_r,a,A_m,w_m,phi_m,C], where:
    A_r,w_r,phi_r = Amplitude, frequency, and angular offset of ripple oscillations.
    a = Scaling factor (found in ELSA TDR).
    A_m,w_m,phi_m = Amplitude, frequency, and angular offset of macro (~icicle length) oscillations.
    C = vertical offset of the icicle.

    parameters_left as array: Fit parameters for the left side of the icicle.
    uncerts_left as array: Uncertainties on left side parameters.
    parameters_right as array: Fit parameters for the right side of the icicle.
    uncerts_right as array: Uncertainties on right side parameters.
    icicle_length as float: Length of icicle in cm.
    '''
    
    #Detect Edges of icicle
    left_init,right_init = EdgeDetect(imageloc,threshold=edgethreshold,kernalsize=kernalsize,bound=detectionbound)
    
    #Correct left and right edges relative to icicle spine
    left_fin,right_fin = SpineCalc(left_init,right_init,threshold=spinethreshold)
    
    #Reverse left and right edges and convert length to cm.
    left_rev = left_fin[::-1]/(ppcm)
    right_rev = right_fin[::-1]/(ppcm)
    
    #Create a space for the z values of the icicle, in cm.
    z_icicle = np.linspace(1,len(left_rev)/(ppcm),len(left_rev))

    #Calculate left and right side fit parameters and uncertainties
    parameters_left,uncerts_left = EdgeFit(left_rev,z_icicle,parguess=parguess,error=error,sigma_abs=sigma_abs,
                                             amplitudethreshold=amplitudethresh,amplituderesolution=amplituderes,
                                              amplitudeiterations=amplitudeiter,ignoreIterate=ignoreIterate,
                                             oscillationFit=oscillationFit)
    parameters_right,uncerts_right = EdgeFit(right_rev,z_icicle,parguess=parguess,error=error,sigma_abs=sigma_abs,
                                             amplitudethreshold=amplitudethresh,amplituderesolution=amplituderes,
                                              amplitudeiterations=amplitudeiter,ignoreIterate=ignoreIterate,
                                             oscillationFit=oscillationFit)
        
    #Calculate length of icicle
    icicle_length = max(z_icicle)
        
    #Returns parameters and icicle length
    return parameters_left,uncerts_left,parameters_right,uncerts_right,icicle_length
