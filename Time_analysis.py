'''
ELSA Icicle functions for fit parameter comparison and plotting. These function will compare 
the amplitude (A_r), frquency (w), frequency offset (phi), and aplitude offset (C_r) 
over the growth of one icicle. 
'''

import numpy as np
import matplotlib.pyplot as plt

#set of functions that plot the various parameters as a function of time and length
def AmpPlot (amplitudes_left, amplitudes_right, amplitudes_left_sigma, amplitudes_right_sigma, times, lengths, icicle_num) : 
    '''
    Plot the amplitude of sinusoidal ridges of the icicle of the icicle as a function of time and length. 

    amplitudes_left : list of the amplitude for the left-hand side of the icicle during growth
    amplitudes_right : list of the amplitude for the right-hand side of the icicle during growth
    amplitudes_left_sigma : list of the  error on the amplitude for the left-hand side of the icicle during growth
    amplitudes_right_sigma : list of the  error on the amplitude for the right-hand side of the icicle during growth
    times : list of time of each photo taken
    lengths : list of lengths of icicle at each photo
    icicle_num : icicle number for identification, string

    Two plots are saved, with four lines, one for each side of the icicle during growth. 
    '''

    #Define four lists for amplitudes of four sides of icicle
    #side 0
    Ar_right = [] 
    Ar_right_sigma = []
    #side 1
    Ar_front = [] 
    Ar_front_sigma = []
    #side 2
    Ar_left = []  
    Ar_left_sigma = []
    #side 3
    Ar_back = []  
    Ar_back_sigma = []

    #time and length arrays for right/left and front/back
    times_rl = []
    times_fb = []
    lengths_rl = []
    lengths_fb = []
    
    for i in range(len(times)) : 
        #Determine what face of icicle is being looked at 
        step_count = i % 4 
        if step_count == 0 : 
            Ar_right.append(amplitudes_right[i])
            Ar_right_sigma.append(amplitudes_right_sigma[i])
            Ar_left.append(amplitudes_left[i])
            Ar_left_sigma.append(amplitudes_left_sigma[i])
            times_rl.append(times[i])
            lengths_rl.append(lengths[i])
        if step_count == 1 :
            Ar_front.append(amplitudes_right[i])
            Ar_front_sigma.append(amplitudes_right_sigma[i])
            Ar_back.append(amplitudes_left[i])
            Ar_back_sigma.append(amplitudes_left_sigma[i])
            times_fb.append(times[i])
            lengths_fb.append(lengths[i])
        if step_count == 2 :
            Ar_right.append(amplitudes_left[i])
            Ar_right_sigma.append(amplitudes_left_sigma[i])
            Ar_left.append(amplitudes_right[i])
            Ar_left_sigma.append(amplitudes_right_sigma[i])
            times_rl.append(times[i])
            lengths_rl.append(lengths[i])
        if step_count == 3 : 
            Ar_front.append(amplitudes_left[i])
            Ar_front_sigma.append(amplitudes_left_sigma[i])
            Ar_back.append(amplitudes_right[i])
            Ar_back_sigma.append(amplitudes_right_sigma[i])
            times_fb.append(times[i])
            lengths_fb.append(lengths[i])

    #plotting 
    plt.figure(figsize = (14, 6))
    plot_name = 'amplitude_plot_' + icicle_num + '.jpg'

    plt.subplot(121)
    plt.errorbar(times_rl, Ar_right, Ar_right_sigma, label = 'Right')
    plt.errorbar(times_rl, Ar_left, Ar_left_sigma, label = 'Left')
    plt.errorbar(times_fb, Ar_front, Ar_front_sigma, label = 'Front')
    plt.errorbar(times_fb, Ar_back, Ar_back_sigma, label = 'Back')
    plt.xlabel('Time ()')
    plt.ylabel('Amplitude ()')
    plt.legend(loc=2)

    plt.subplot(122)
    plt.errorbar(lengths_rl, Ar_right, Ar_right_sigma, label = 'Right')
    plt.errorbar(lengths_rl, Ar_left, Ar_left_sigma, label = 'Left')
    plt.errorbar(lengths_fb, Ar_front, Ar_front_sigma, label = 'Front')
    plt.errorbar(lengths_fb, Ar_back, Ar_back_sigma, label = 'Back')
    plt.xlabel('Icicle Length ()')
    plt.ylabel('Amplitude ()')
    plt.legend(loc=2)

    plt.suptitle('Icicle sinusoid amplitude')
    plt.savefig(plot_name)

    return

def FrequencyPlot (frequencies_left, frequencies_right, frequencies_left_sigma, frequencies_right_sigma, times, lengths, icicle_num) : 
    '''
    Plot the frequency of the sinusoidal ridges of the icicle as a function of time and length. 

    frequencies_left : list of the frequencies for the left-hand side of the icicle during growth
    frequencies_right : list of the frequencies for the right-hand side of the icicle during growth
    frequencies_left_sigma : list of the  error on the frequencies for the left-hand side of the icicle during growth
    frequencies_right_sigma : list of the  error on the frequencies for the right-hand side of the icicle during growth
    times : list of time of each photo taken
    lengths : list of lengths of icicle at each photo
    icicle_num : icicle number for identification, string

    Frequencies are averages for the different sides fo the icicle.
    Two plots are saved, with four lines, one for each side of the icicle during growth. 
    '''
    #average frequency between right and left of icicle
    frequencies = (np.array(frequencies_left) + np.array(frequencies_right)) / 2
    frequencies_sigma = np.sqrt(np.array(frequencies_left_sigma) ** 2 + np.array(frequencies_right_sigma) ** 2) / 2

    #plotting 
    plt.figure(figsize = (14, 6))
    plot_name = 'frequency_plot_' + icicle_num + '.jpg'

    plt.subplot(121)
    plt.errorbar(times, frequencies, frequencies_sigma)
    plt.xlabel('Time ()')
    plt.ylabel('Frequency ()')

    plt.subplot(122)
    plt.errorbar(lengths, frequencies, frequencies_sigma)
    plt.xlabel('Icicle Length ()')
    plt.ylabel('Frequency ()')

    plt.suptitle('Icicle sinusoid frequency')
    plt.savefig(plot_name)
    return

def OffsetPlot (offsets_left, offsets_right, offsets_left_sigma, offsets_right_sigma, times, lengths, icicle_num) : 
    '''
    Plot the frequency offset of the sinusoidal ridges of the icicle as a function of time and length. 

    offsets_left : list of the offsets for the left-hand side of the icicle during growth
    offsets_right : list of the offsets for the right-hand side of the icicle during growth
    offsets_left_sigma : list of the  error on the offsets for the left-hand side of the icicle during growth
    offsets_right_sigma : list of the  error on the offsets for the right-hand side of the icicle during growth
    times : list of time of each photo taken
    lengths : list of lengths of icicle at each photo
    icicle_num : icicle number for identification, string

    Two plots are saved, with four lines, one for each side of the icicle during growth. 
    '''
    #plotting 
    plt.figure(figsize = (14, 6))
    plot_name = 'frequencyoffset _offset_plot_' + icicle_num + '.jpg'

    plt.subplot(121)
    plt.errorbar(times, offsets_left, offsets_left_sigma, label = 'Left')
    plt.errorbar(times, offsets_right_sigma, offsets_right_sigma, label = 'Right')
    plt.xlabel('Time ()')
    plt.ylabel('Phi ()')
    plt.legend(loc=2)

    plt.subplot(122)
    plt.errorbar(lengths, offsets_left, offsets_left_sigma, label = 'Left')
    plt.errorbar(lengths, offsets_right, offsets_right_sigma, label = 'Right')
    plt.xlabel('Icicle Lengths ()')
    plt.ylabel('Phi ()')
    plt.legend(loc=2)

    plt.suptitle('Icicle sinusoid frequency offset')
    plt.savefig(plot_name)
    return

def ConstantPlot (constants_left, constants_right, constants_left_sigma, constants_right_sigma, times, lengths, icicle_num) : 
    '''
    Plot the amplitude constant offset offset of the sinusoidal ridges of the icicle as a function of time and length. 

    constants_left : list of the constants for the left-hand side of the icicle during growth
    constants_right : list of the constants for the right-hand side of the icicle during growth
    constants_left_sigma : list of the  error on the constants for the left-hand side of the icicle during growth
    constants_right_sigma : list of the  error on the constants for the right-hand side of the icicle during growth
    times : list of time of each photo taken
    lengths : list of lengths of icicle at each photo
    icicle_num : icicle number for identification, string

    Two plots are saved, with four lines, one for each side of the icicle during growth. 
    '''
    #plotting 
    plt.figure(figsize = (14, 6))
    plot_name = 'amplitude_offset_plot_' + icicle_num + '.jpg'

    plt.subplot(121)
    plt.errorbar(times, constants_left, constants_left_sigma, label = 'Left')
    plt.errorbar(times, constants_right, constants_right_sigma, label = 'Right')
    plt.xlabel('Time ()')
    plt.ylabel('C_r ()')
    plt.legend(loc=2)

    plt.subplot(122)
    plt.errorbar(lengths, constants_left, constants_left_sigma, label = 'Left')
    plt.errorbar(lengths, constants_right, constants_right_sigma, label = 'Right')
    plt.xlabel('Icicle Lengths ()')
    plt.ylabel('C_r ()')
    plt.legend(loc=2)

    plt.suptitle('Icicle sinusoid amplitude constant')
    plt.savefig(plot_name)
    return 



def TimeAnalysis (params, errors, times, lengths, icicle_num) : 
    '''

    params : 2D list of parameter outputs [[amplitudes_right], [amplitudes_left] [frequencies], [offsets], [constants]]
    errors : 2D list of parameter errors
    times : list of time of each photo taken
    lengths : list of lengths of icicle at each photo
    icicle_num : integer indicating what icicle is being analysed

    '''
    icicle_num_str = str(icicle_num)
    A_right, A_left, w, phi, C_r = params[0], params[1], params[2], params[3]


    AmpPlot (amplitudes_left, amplitudes_right, amplitudes_left_sigma, amplitudes_right_sigma, times, lengths, icicle_num)

    return 