
'''
ELSA Icicle Fit Script to fit the left and right edges of the icicle found using OpenCV
Performed using scipy optimize to fit using a least squares method.
This script has 5 functions; DistilledFit, SinusoidalFit, AmplitudeGuess, OffsetGuess, and EdgeFit, where the first 4 are used in
EdgeFit. Use help(EdgeFit) for more information.
'''

#Import required libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import welch

def DistilledFit(z,a):
    '''
    Distilled water response function, defined by Equation (8) in section 2.1.3 of ELSA TDR.
    This function is automatically called in EdgeFit, and does not need to be called independently.
    '''
    response = a*(4/3)*((z/a)**(1/2)+2)*((z/a)**(1/2)-1)**(1/2)
    return response

def SinusoidalFit(z,A_r,w,phi,C):
    '''
    Model for oscillations in icicle edges, introduced in section 2.3 of ELSA TDR.
    This function is automatically called in EdgeFit, and does not need to be called independently.
    '''
    ripple = A_r*np.sin(w*z+phi)
    offset = C
    return ripple + offset

def AmplitudeGuess(residuals,z,threshold=0.01,resolution=3,iterate=4):
    '''
    Function to calculate an accurate "guess" of the oscillation amplitude and frequency.
    Performed by finding indices where the gradient of the response is close to 0, then evaluating the difference in
    amplitude of the response at these indices. The average of all amplitudes calculated over however many iterations
    are called is then returned.
    Takes the following arguments:
    
    residuals as array: Residuals of icicle edges after distilled water fit.
    z as array: z values of the icicle as in EdgeFit
    threshold as float: How close to 0 a point in the gradient has to be to be considered a critical point. Defaults to 0.01
    resolution as integer: How many indices to skip after finding a critical point to avoid finding two near-adjacent critical points. Defaults to 3.
    iterate as integer: How many iterations to average the amplitude guesses over. Defaults to 4.
    
    And returns the following:
    
    Amp_avg as float: Average amplitude calculated for parameter guess for fitting the residual to a sinusoid.
    
    Note that this function is called automatically in EdgeFit, and thus does not need to be called independently.
    '''
    grad = np.gradient(residuals,z)
    
    runs = 0
    peaknum = 0
    ind1 = 0
    ind2 = 0
    Amps = []
    freqs = []
    for i in range(len(grad)):
        if runs < iterate:
            if grad[i] < threshold and grad[i] > -1*threshold:
                if peaknum == 0:
                    ind1 = i
                    peaknum = 1
                elif peaknum == 1:
                    ind2 = i
                    amp_temp = (residuals[ind1]-residuals[ind2])/2
                    Amps.append(amp_temp)
                    freq_temp = 2*(z[ind2]-z[ind1])
                    freqs.append(freq_temp)
                    peaknum = 0
                    runs += 1
        elif runs >= iterate:
            break
    Amp_avg = sum(Amps)/iterate
    Freq_avg = sum(freqs)/iterate
    return Amp_avg,Freq_avg

def OffsetGuess(residuals,z):
    '''
    Function to guess the vertical offset of the oscillations of the icicle growth.
    Simply returns the first value of the residual response after distilled water fit.
    This function is called automatically in EdgeFit and does not need to be called independently.
    '''
    c_guess = residuals[0]
    return c_guess

def EdgeFit(response,z,parguess=[],error=0,sigma_abs = True,
            bounds=[],amplitudethreshold = 0.01,amplituderesolution = 3,amplitudeiterations = 4):
    '''
    Fit the position vectors of the icicle edges to the response function found in section 2.3 of the ELSA TDR.
    Takes the following arguments:

    response as array: Icicle edge positions as a function of z.
    z as array: z values along edge of icicle, where z=0 is the icicle tip, and z=zmax is the icicle base.
    parguess as array: guess values for parameters, as follows, from section 2.3 of ELSA TDR: [A_r,w,phi,C_r]. Defaults to [A_guess,w_guess,0,C_guess], where A_guess, w_guess, and C_guess are calculated by the AmplitudeGuess, FrequencyGuess, and OffsetGuess functions, respectively.
    error as array-like: Error on response values. Defaults to max(response)/(len(response))**(1/2)
    sigma_abs as Boolean: Whether or not to use absolute_sigma in curve_fit. Defaults to True.
    bounds as 2 arrays: Lower and upper bounds on fit parameters
    amplitudethreshold as float: Thresholding value for AmplitudeGuess function. Defaults to 0.01.
    amplituderesolution as int: Resolution value for AmplitudeGuess Function. Defaults to 3.
    amplitudeiterations as int: Number of iterations to average over for the AmplitudeGuess function. Defaults to 4.

    And returns the following:

    params as array: Fit parameters calculated using scipy.optimize.curve_fit. Parameters are as follows, from section 2.3 of ELSA TDR: [A_r,w,phi,C_r]. In addition, includes a, the scaling factor for the ideal icicle.
    uncerts as array: Uncertainties from covariance matrix for Fit performed with scipy.optimize.curve_fit.
    '''

    if error == 0:
        error=(max(response)/(len(response))**(1/2))*np.ones(len(response))
            
    if bounds == []:
        bounds = ((-max(response),0,-np.pi/2,-20),(max(response),len(z)/10,np.pi/2,20))
    
    dist_fit,dist_cov = curve_fit(DistilledFit,z,response,p0=[0.01],sigma=error,absolute_sigma=sigma_abs)
    
    dist_resp = DistilledFit(z,dist_fit)
    
    res = response - dist_resp
    
    if parguess == []:
        amp_guess,w_guess = AmplitudeGuess(res,z,amplitudethreshold,amplituderesolution,amplitudeiterations)
        c_guess = OffsetGuess(res,z)
        parguess = (amp_guess,w_guess,0,c_guess)
    
    error_residual = (error**2+(dist_cov[0][0])**2)**(1/2)
    
    print(parguess)
    
    params_sine, pcov_sine = curve_fit(SinusoidalFit,z,res,p0=parguess,sigma=error_residual,absolute_sigma = sigma_abs,bounds=bounds)
    params = [params_sine[0],params_sine[1],params_sine[2],params_sine[3],dist_fit[0]]
    uncerts = [pcov_sine[0][0],pcov_sine[1][1],pcov_sine[2][2],pcov_sine[3][3],dist_cov[0][0]]
    
    return params,uncerts

