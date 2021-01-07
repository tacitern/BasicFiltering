"""

"""
import numpy as np


def abs_fft(Fs, data):
    """

    :param Fs:
    :param data:
    :return:
    """
    x = np.fft.fft(data)
    x = 1/Fs * x
    f = []
    for i in range(len(x)):
        f.append((-(len(x)/2) + i)*Fs/len(x))

    abs_mag = list(np.sqrt(x.real**2 + x.imag**2))

    return (f, abs_mag[int(len(x)/2):] + abs_mag[:int(len(x)/2)])


def abs_fft_dB(Fs, data):
    """

    :param Fs:
    :param data:
    :return:
    """
    f, data = abs_fft(Fs, data)

    datadb = []
    for i in range(len(data)):
        datadb.append(20 * np.log10(data[i]))

    return (f, datadb)


def abs_fft_dB_rel(Fs, data):
    """

    :param Fs:
    :param data:
    :return:
    """
    f, data = abs_fft(Fs, data)

    ref = max(data)

    datadb = []
    for i in range(len(data)):
        datadb.append(20 * np.log10(data[i] / ref))

    return (f, datadb)
