import matplotlib.pyplot as plt


def convolution(input1, input2, tr=True):
    """
    convolution preforms convolution on two given lists of data through use of a circular buffer routine.
    The smaller of the two lists is used as a a set of static values while the larger is fed into and out of
    the circular buffer a sample at a time.
    :param input1: list of data to convolve
    :param input2: list of data to convolve
    :param tr: Transient Response; If true zeros are added to the end of the larger input list
               to allow for the circular buffer used for the convolution to empty all input data
    :return: data_out: A list data corresponding to the convolution of input1 and input2
    """
    # Pick which input is used for the circular buffer
    if input1 > input2:
        cirbuffer = [0] * len(input2)
        static = input2
        data_in = input1
    elif input1 < input2:
        cirbuffer = [0] * len(input1)
        static = input1
        data_in = input2
    else:
        cirbuffer = [0] * len(input1)
        static = input1
        data_in = input2

    # If true extra zeros are added to the end of data_in to allow transient of unloading the buffer
    if tr == True:
        data_in = data_in + [0]*len(cirbuffer)  # Adding zeros to the end of the input data to flush the buffer.
                                                # This shows the transient response as the buffer empties

    data_out = []
    cirindex = 0  # current sample index in the circular buffer

    # A circular buffer routine is used to accomplish the convolution
    for i in range(len(data_in)):
        accum = 0  # Convolution is a MAC (Multiply Accumulate) process.
                   # accum sums all input data multiplications with the static array

        cirbuffer[cirindex] = data_in[i]

        for j in range(len(cirbuffer)):
            if j <= cirindex:
                accum = accum + static[j] * cirbuffer[cirindex - j]
            else:
                accum = accum + static[j] * cirbuffer[len(cirbuffer) + (cirindex - j)]

        data_out.append(accum)

        # adjust cirindex to the next location in the circular buffer
        if cirindex < len(cirbuffer) - 1:
            cirindex = cirindex + 1
        else:
            cirindex = 0

    return data_out


if __name__ == '__main__':
    x1 = [1]*10
    x2 = [1]*15

    out = convolution(x1, x2)

    plt.plot(out)
    plt.show()

