import BasicFiltering.Functions.Convolution.Convolution as conv


def filter(data_in, firfiltertaps, tr=True):
    """
    'filter' preforms convolution on the input data list with a set of FIR filter taps.
    All digital filtering is essentially convolution on a set of incoming data
    with a set of filter taps. In the case of FIR filtering there is no feedback required
    allowing a straight MAC (Multiply Accumulate) process can be used. The convolution function
    in BasicFiltering/Functions/Convolution/Convolution.py preforms this task.
    :param data_in:         List of incoming data to be filtered by firfiltertaps
    :param firfiltertaps:   List of Taps selected to filter data_in
    :param tr: Transient Response; If true zeros are added to allow
               for the circular buffer used for the filtering to empty all input data
    :return: A list data corresponding to the filtering of data_in with firfiltertaps
    """

    return conv.convolution(data_in, firfiltertaps, tr)


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    x1 = [1]*10
    x2 = [1]*15

    out = filter(x1, x2)

    plt.plot(out)
    plt.show()

