
'''
ELSA Icicle Fit Script to fit the left and right edges of the icicle found using OpenCV
Performed using scipy optimize to fit using a least squares method.
This script has 7 functions; DistilledFit, SinusoidalFit, AmplitudeGuess, PhiGuess, OffsetGuess, MacroSineFit, and EdgeFit, where the first 6 are used in EdgeFit. Use help(EdgeFit) for more information.
'''

#Import required libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.ndimage import gaussian_filter

def DistilledFit(z,a):
    '''
    Distilled water response function, defined by Equation (8) in section 2.1.3 of ELSA TDR.
    This function is automatically called in EdgeFit, and does not need to be called independently.
    '''
    response = a*(4/3)*((z/a)**(1/2)+2)*((z/a)**(1/2)-1)**(1/2)
    return response

def SinusoidalFit(z,A_r,w,phi):
    '''
    Model for oscillations in icicle edges, introduced in section 2.3 of ELSA TDR.
    This function is automatically called in EdgeFit, and does not need to be called independently.
    '''
    ripple = A_r*np.sin(w*z+phi)
    return ripple

def AmplitudeGuess(residuals,z,threshold=0.01,resolution=3,iterate=4,fullIcicle=False):
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
    fullIcicle as boolean: Whether to iterate over the full icicle. Defaults to false.
    
    And returns the following:
    
    Amp_avg as float: Average amplitude calculated for parameter guess for fitting the residual to a sinusoid.
    Amp_std as float: Standard deviation of amplitude guesses.
    Freq_avg as float: Average frequency of oscillations calculated for parameter guess for sinusoidal fitting.
    Freq_std as float: Standard deviation of frequency guesses.
    
    
    Note that this function is called automatically in EdgeFit, and thus does not need to be called independently.
    '''
    gf_residuals = gaussian_filter(residuals,sigma=resolution)
    grad = np.gradient(gf_residuals,z)
    grad2 = np.gradient(grad,z)
    
    runs = 0
    peaknum = 0
    ind1 = 0
    ind2 = 0
    Amps = []
    freqs = []
    for i in range(resolution,len(grad)):
        if runs < iterate and fullIcicle == False:
            left_slope = np.mean(grad[i-resolution:i])
            right_slope = np.mean(grad[i:i+resolution])
            if grad[i] < threshold and grad[i] > -1*threshold and left_slope*right_slope < 0 \
            and (grad[i]*grad[i+1] < 0 or grad[i]*grad[i-1] < 0 or grad[i-1]*grad[i+1] < 0):
                if peaknum == 0:
                    ind1 = i
                    peaknum = 1
                elif peaknum == 1 and grad2[i]*grad2[ind1] < 0:
                    ind2 = i
                    amp_temp = (residuals[ind1]-residuals[ind2])/2
                    Amps.append(abs(amp_temp))
                    freq_temp = np.pi/((z[ind2]-z[ind1]))
                    freqs.append(freq_temp)
                    peaknum = 0
                    runs += 1
                    ind1 = 0
                    ind2 = 0
        elif runs >= iterate:
            break
        elif fullIcicle == True:
            left_slope = np.mean(grad[i-resolution:i])
            right_slope = np.mean(grad[i:i+resolution])
            if grad[i] < threshold and grad[i] > -1*threshold and left_slope*right_slope < 0 \
            and (grad[i]*grad[i+1] < 0 or grad[i]*grad[i-1] < 0 or grad[i-1]*grad[i+1] < 0):
                if peaknum == 0:
                    ind1 = i
                    peaknum = 1
                elif peaknum == 1 and grad2[i]*grad2[ind1] < 0:
                    ind2 = i
                    amp_temp = (residuals[ind1]-residuals[ind2])/2
                    Amps.append(abs(amp_temp))
                    freq_temp = np.pi/((z[ind2]-z[ind1]))
                    freqs.append(freq_temp)
                    peaknum = 0
                    ind1 = 0
                    ind2 = 0

    Amp_avg = np.mean(Amps)
    Freq_avg = np.mean(freqs)
    Amp_std = np.std(Amps)
    Freq_std = np.std(freqs)
    return Amp_avg,Amp_std,Freq_avg,Freq_std

def PhiGuess(residuals,z,wguess):
    '''
    Function to guess the angular offset of the oscillations of the icicle growth.
    This function is called automatically in EdgeFit and does not need to be called independently.
    '''
    gf_residuals = gaussian_filter(residuals,sigma=15)
    grad = np.gradient(gf_residuals,z)
    grad2 = np.gradient(grad,z)
    for j in range(0,len(grad)):
        if grad[j] == 0 or grad[j]*grad[j-1] < 0:
            crit = j
            concave = grad2[j]
            if concave != 0:
                break
    if concave < 0:
        phi_guess = wguess/2 - z[crit]
    else:
        phi_guess = z[crit]-wguess/2
    return phi_guess

def OffsetGuess(residuals,z):
    '''
    Function to guess the vertical offset of the oscillations of the icicle growth.
    Simply returns the first value of the residual response after distilled water fit.
    This function is called automatically in EdgeFit and does not need to be called independently.
    '''
    c_guess = residuals[0]
    return c_guess

def MacroSineFit(z,A_L,w_L,phi_L,C):
    '''
    Model for large-scale oscillations in icicle edges, discovered in earlier analysis of icicles from the Icicle Atlas.
    This function is automatically called in EdgeFit, and does not need to be called independently.
    '''
    ripple = A_L*np.sin(w_L*z+phi_L)
    offset = C
    return ripple + offset

def EdgeFit(response,z,parguess=[],error=0,sigma_abs = True,
            bounds=[],amplitudethreshold = 0.01,amplituderesolution = 3,amplitudeiterations = 4,ignoreIterate = False,
           oscillationFit = True):
    '''
    Fit the position vectors of the icicle edges to the response function found in section 2.3 of the ELSA TDR.
    Takes the following arguments:

    response as array: Icicle edge positions as a function of z.
    z as array: z values along edge of icicle, where z=0 is the icicle tip, and z=zmax is the icicle base.
    parguess as array: guess values for parameters, as follows, from section 2.3 of ELSA TDR: [A_r,w,phi,C_r]. Defaults to [A_guess,w_guess,0,C_guess], where A_guess, w_guess, and C_guess are calculated by the AmplitudeGuess, FrequencyGuess, and OffsetGuess functions, respectively.
    error as array-like: Error on response values. Defaults to abs(z[1]-z[0])/2
    sigma_abs as Boolean: Whether or not to use absolute_sigma in curve_fit. Defaults to True.
    bounds as 2 arrays: Lower and upper bounds on fit parameters
    amplitudethreshold as float: Thresholding value for AmplitudeGuess function. Defaults to 0.01.
    amplituderesolution as int: Resolution value for AmplitudeGuess Function. Defaults to 3.
    amplitudeiterations as int: Number of iterations to average over for the AmplitudeGuess function. Defaults to 4.
    ignoreIterate as boolean: Whether to continue iteration of amplitude guesses after the fixed number of iterations given in amplitudeiterations. Defaults to False.
    oscillationFit as boolean: Whether to perform a fit on the icicle oscillations rather than just returning the parameter guesses. Defaults to True.
    
    And returns the following:

    params as array: Fit parameters calculated using scipy.optimize.curve_fit. Parameters are as follows, from section 2.3 of ELSA TDR: [A_r,w,phi,C_r]. In addition, includes a, the scaling factor for the ideal icicle.
    uncerts as array: Uncertainties from covariance matrix for Fit performed with scipy.optimize.curve_fit.
    '''

    if error == 0:
        error=(abs((z[1]-z[0])/2))*np.ones(len(response))
            
    if bounds == []:
        bounds = ((-max(response),0,-np.pi/2),(max(response),len(z)/10,np.pi/2))
    
    dist_fit,dist_cov = curve_fit(DistilledFit,z,response,p0=[0.01],sigma=error,absolute_sigma=sigma_abs)
    
    dist_resp = DistilledFit(z,dist_fit)
    
    res = response - dist_resp
    
    plt.plot(z,res)
    plt.show()
    
    error_residual = (error[0]**2+(dist_cov[0][0])**2)**(1/2)*np.ones(len(res))
    
    c_guess = OffsetGuess(res,z)
    res_amp_guess = (abs(max(res)-min(res))/2)
    res_omega_guess = 2*np.pi/len(res)
    res_phi_guess = (z[np.argmax(res)])
    
    res_p0 = [res_amp_guess,res_omega_guess,res_phi_guess,c_guess]
    
    print(res_p0)
    
    macro_fit,macro_cov = curve_fit(MacroSineFit,z,res,p0=res_p0,sigma=error_residual,absolute_sigma=sigma_abs,
                                    bounds=([res_amp_guess/2,res_omega_guess/2,-1*len(res),c_guess/3],
                                            [3*res_amp_guess/2,2*res_omega_guess,len(res),3*c_guess]))
    
    macro_resp = MacroSineFit(z,macro_fit[0],macro_fit[1],macro_fit[2],macro_fit[3])
    
    res2 = res - macro_resp
    
    res_bulk = res2[int(len(res)/5):len(res)]
    z_bulk = z[int(len(res)/5):len(res)]
    
    if parguess == []:
        amp_guess,amp_std,w_guess,w_std = AmplitudeGuess(res_bulk,z_bulk,amplitudethreshold,amplituderesolution,amplitudeiterations,
                                                        fullIcicle=ignoreIterate)
        phi_guess = PhiGuess(res2,z,w_guess)
        parguess = (amp_guess,w_guess,phi_guess)
    
    
    error_residual2 = (error_residual[0]**2+(macro_cov[0][0])**2+(macro_cov[1][1])**2
                      +(macro_cov[2][2])**2+(macro_cov[3][3])**2)**(1/2)*np.ones(len(res_bulk))
    
    if oscillationFit == True:
        params_sine, pcov_sine = curve_fit(SinusoidalFit,z_bulk,res_bulk,p0=parguess,sigma=error_residual2,
                                           absolute_sigma = sigma_abs,bounds=bounds)
    
        params = [params_sine[0],params_sine[1],params_sine[2],dist_fit[0],macro_fit[0],macro_fit[1],macro_fit[2],macro_fit[3]]
        uncerts = [(pcov_sine[0][0])**(1/2),(pcov_sine[1][1])**(1/2),(pcov_sine[2][2])**(1/2),(dist_cov[0][0])**(1/2),
                   (macro_cov[0][0])**(1/2),(macro_cov[1][1])**(1/2),(macro_cov[2][2])**(1/2),(macro_cov[3][3])**(1/2)]
    elif oscillationFit == False:
        params = [parguess[0],parguess[1],parguess[2],dist_fit[0],macro_fit[0],macro_fit[1],macro_fit[2],macro_fit[3]]
        uncerts = [amp_std,w_std,abs(z_bulk[0]-z_bulk[1]),(dist_cov[0][0])**(1/2),
                   (macro_cov[0][0])**(1/2),(macro_cov[1][1])**(1/2),(macro_cov[2][2])**(1/2),(macro_cov[3][3])**(1/2)]
        
    return params,uncerts

