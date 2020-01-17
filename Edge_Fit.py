
'''
ELSA Icicle Fit Script to fit the left and right edges of the icicle found using OpenCV
Performed using scipy optimize to fit using a least squares method.
This script has 2 functions, EdgeFit and ResponseFit, with the latter being used in the former.
Use help(EdgeFit) for more information.
'''

#Import required libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def ResponseFit(z,A_r,w,phi,C):
    '''
    Response function, as defined in the technical report, section 2.3.
    This function is automatically called in EdgeFit, and does not need to be called independently.
    '''
    ideal = (4/3)*(z**(1/2)+2)*(z**(1/2)-1)**(1/2)
    ripple = A_r*np.sin(w*z+phi)
    offset = C
    return ideal + ripple + offset

def ScaleParam(response,z):
    '''
    Response scaling function, defined as a in the technical report, section 2.1.3.
    This function is automatically called in EdgeFit, and does not need to be called independently.
    '''
    arga = max(response)/(2*len(z))
    argb = 2*np.arctan(arga)
    trig = (np.sin(argb))**4
    a = z*trig
    
    return a
    

def EdgeFit(response,z,parguess=[],error=0,sigma_abs = True,
            bounds=[]):
    '''
    Fit the position vectors of the icicle edges to the response function found in section 2.3 of the ELSA TDR.
    Takes the following arguments:

    response as array: Icicle edge positions as a function of z.
    z as array: z values along edge of icicle, where z=0 is the icicle tip, and z=zmax is the icicle base.
    parguess as array: guess values for parameters, as follows, from section 2.3 of ELSA TDR: [A_r,w,phi,C_r].
    Defaults to [(max(response)-min(response))/5,len(response)/20,0,0]
    error as array-like: Error on response values. Defaults to max(response)/(len(response))**(1/2)
    sigma_abs as Boolean: Whether or not to use absolute_sigma in curve_fit. Defaults to True.
    bounds as 2 arrays: Lower and upper bounds on fit parameters

    And returns the following:

    params as array: Fit parameters calculated using scipy.optimize.curve_fit. Parameters are as follows, from section 2.3
    of ELSA TDR: [A_r,w,phi,C_r].
    pcov as array: Covariance matrix for Fit performed with scipy.optimize.curve_fit.
    '''
    a = ScaleParam(response,z)
    print(a)
    
    if error == 0:
        error=(max(response)/(len(response))**(1/2))*np.ones(len(response))
        
    if parguess == []:
        parguess = ((max(response)-min(response))/5,len(response)/20,0,0,a)
    
    if bounds == []:
        bounds = ((0,0,-np.pi/2,-2,a/2),(max(response),len(z)/10,np.pi/2,2,3*a/2))
    
    
    z_prep = np.divide(np.array(z),a)
    response_prep = np.array(response)
    
    params, pcov = curve_fit(ResponseFit,z_prep,response_prep,p0=parguess,sigma=error,absolute_sigma = sigma_abs,bounds=bounds)
    
    return params,pcov

