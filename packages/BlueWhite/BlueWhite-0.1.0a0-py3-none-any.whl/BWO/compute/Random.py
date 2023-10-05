import numpy
import scipy


def ZeroToHundred():
    x = numpy.arange(0, 101)
    pdf = scipy.stats.norm.pdf(x, loc=50, scale=10)
    return numpy.random.choice(x, p=pdf / pdf.sum())


if __name__ == '__main__':
    print(ZeroToHundred())
