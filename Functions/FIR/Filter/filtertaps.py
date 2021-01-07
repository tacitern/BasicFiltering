"""
'filtertaps.py'
The Functions in this file generate Finite Impulse Response(FIR) filter taps.

Each function has a parameter N. The N parameter is required to be an odd number.
This allows all functions to produce even symmetry, about 0, taps which will produce
taps that work for all filter types.

Allpass, Highpass and Bandstop filters require a tap at 0. To achieve linear phase
filters the taps must have symmetry about 0. The easiest way to maintain linear phase
and produces taps which work for all filter an odd number is enforced for the parameter
N. This can be overridden by using the 'min_tap' and 'max_tap' parameters
"""
import numpy as np


def allpass_taps(N=None, min_tap=None, max_tap=None):
    """

    :param N: The number of filter taps. The N parameter enforces linear phase filters.
              This is accomplished by maintaining an even symmetry about 0. Because
              allpass filters require a tap at 0, an odd number of taps is enforced for N
    :param min_tap: Lowest Tap location
    :param max_tap: Highest Tap location
    :return: list of filter taps
    """
    if int(N):
        if N % 2 == 0:
            raise Exception('N is required to be an odd number for allpass filters')
        else:
            N = range(int(-(N-1)/2), int((N-1)/2 + 1))
    elif not int(min_tap) and not int(max_tap):
        N = range(min_tap, max_tap + 1)
    else:
        raise Exception("'N' or 'min_tap' and 'max_tap' must have values")

    taps = []
    for i in N:
        if i != 0:
            taps.append(0)
        else:
            taps.append(1)

    return taps


def lowpass_taps(wc, N=None, min_tap=None, max_tap=None):
    """

    :param wc:
    :param N:
    :param min_tap:
    :param max_tap:
    :return:
    """
    if int(N):
        if N % 2 == 0:  # even taps are allowed. values are at a 0.5 shift to maintain symmetry
            n = []
            for i in range(N):
                n.append(-(N-1)/2 + i)
            N = n
        else:
            N = range(int(-(N-1)/2), int((N-1)/2 + 1))
    elif int(min_tap) and int(max_tap):
        N = range(min_tap, max_tap+1)
    else:
        raise Exception("'N' or 'min_tap' and 'max_tap' must have values")

    taps = []
    for i in N:
        if i != 0:
            taps.append(np.sin(wc * i) / (np.pi * i))
        else:
            taps.append(wc/np.pi)

    return taps


def highpass_taps(wc, N=None, min_tap=None, max_tap=None):
    """

    :param wc:
    :param N:
    :param min_tap:
    :param max_tap:
    :return:
    """
    if int(N):
        if N % 2 == 0:
            raise Exception('N is required to be an odd number for highpass filters')
        else:
            N = range(int(-(N-1)/2), int((N-1)/2 + 1))
    elif int(min_tap) and int(max_tap):
        N = range(min_tap, max_tap+1)
    else:
        raise Exception("'N' or 'min_tap' and 'max_tap' must have values")

    taps = []
    for i in N:
        if i != 0:
            taps.append(-np.sin(wc * i) / (np.pi * i))
        else:
            taps.append(1 - wc/np.pi)

    return taps


def bandpass_taps(wa, wb, N=None, min_tap=None, max_tap=None):
    """

    :param wa:
    :param wb:
    :param N:
    :param min_tap:
    :param max_tap:
    :return:
    """
    if int(N):
        if N % 2 == 0:  # even taps are allowed. values are at a 0.5 shift to maintain symmetry
            n = []
            for i in range(N):
                n.append(-(N-1)/2 + i)
            N = n
        else:
            N = range(int(-(N-1)/2), int((N-1)/2 + 1))
    elif int(min_tap) and int(max_tap):
        N = range(min_tap, max_tap+1)
    else:
        raise Exception("'N' or 'min_tap' and 'max_tap' must have values")

    taps = []
    for i in N:
        if i != 0:
            taps.append( (np.sin(wb * i) - np.sin(wa * i)) / (np.pi * i))
        else:
            taps.append(wb/np.pi - wa/np.pi)

    return taps


def bandstop_taps(wa, wb, N=None, min_tap=None, max_tap=None):
    """

    :param wa:
    :param wb:
    :param N:
    :param min_tap:
    :param max_tap:
    :return:
    """
    if int(N):
        if N % 2 == 0:
            raise Exception('N is required to be an odd number for bandstop filters')
        else:
            N = range(int(-(N-1)/2), int((N-1)/2 + 1))
    elif int(min_tap) and int(max_tap):
        N = range(min_tap, max_tap+1)
    else:
        raise Exception("'N' or 'min_tap' and 'max_tap' must have values")

    taps = []
    for i in N:
        if i != 0:
            taps.append(-1*(np.sin(wb * i) - np.sin(wa * i)) / (np.pi * i))
        else:
            taps.append(1 - (wb/np.pi - wa/np.pi))

    return taps


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    import BasicFiltering.Functions.FFT.fft as fft
    import BasicFiltering.Functions.FIR.Filter.filter as filt

    fs = 1000

    delta = [1] + [0]*1000

    lpf = lowpass_taps(2*np.pi*100/fs, 41)

    lpf = filt.firfilter(delta, lpf)

    f, data = fft.abs_fft_dB_rel(fs, lpf)

    plt.plot(f, data)
    plt.show()

    sine = []
    for i in range(1000):
        sine.append(np.cos(2*np.pi*98.5*i/fs))

    out = filt.firfilter(sine, lpf)
    plt.plot(sine)
    plt.plot(out)
    plt.show()


    hpf = highpass_taps(2 * np.pi * 100 / fs, 51)

    hpf = filt.firfilter(delta, hpf)

    f, data = fft.abs_fft_dB_rel(fs, hpf)

    plt.plot(f, data)
    plt.show()



    bpf = bandpass_taps(2 * np.pi * 100 / fs, 2 * np.pi * 150 / fs, 50)

    bpf = filt.firfilter(delta, bpf)

    f, data = fft.abs_fft_dB_rel(fs, bpf)

    plt.plot(f, data)
    plt.show()



    bsf = bandstop_taps(2 * np.pi * 100 / fs, 2 * np.pi * 150 / fs, 51)

    bsf = filt.firfilter(delta, bsf)

    f, data = fft.abs_fft_dB_rel(fs, bsf)

    plt.plot(f, data)
    plt.show()
