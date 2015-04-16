"""Example how to use ndiminterpolation.py"""

__author__ = "Robert Nikutta <robert.nikutta@gmail.com>"
__version__ = '20150416'

import numpy as N
import matplotlib
import pylab as p
import ndiminterpolation

def example(plot=True,number=1000):

    import pylab as p
    import matplotlib

    """Example on how to use class NdimInterpolation.

    Usage
    -----
      ipython --pylab
      In[0]: import example
      In[1]: ip, datacube, theta, mywave = example.example()
             # n-dim interpolation object, 3d-cube, sequences of unique parameter values, array of interpolation values

    Parameters
    ----------
    plot : bool
        If True (default), will display a visualization of the data
        hypercube. Click a few times on the figure to move through the
        wavelength slices. If False, the figure won't be displayed.

    number : int or None
        If not None a benchmark of the interpolation speed will be
        performed, with number repetitions. Default: number=1000.

    """

    ### Generate some f(x,y,wave) data
    # two fantasy parameters and a wavelength array
    x = N.linspace(-2,2,100)       # unique ascending list of parameter1 values
    y = N.linspace(-1,1.5,60)      # unique ascending list of parameter2 values
    wave = N.linspace(0.1,3.,10)   # wavelength list

    # sequence of parameter arrays (each a unique sequence)
    theta = N.array((x,y,wave))

    # hypercube to interpolate on
    datacube = N.zeros((x.size,y.size,wave.size))
    X, Y = N.meshgrid(x,y);
    for j,w in enumerate(wave):
        # 2d Gaussian whose center moves along x with increasing wavelength, i.e. a 3-d hypercube
        datacube[...,j] = N.exp(-N.sqrt(X**2+(Y-w)**2)).T

    xmin, xmax = theta[0].min(), theta[0].max()
    ymin, ymax = theta[1].min(), theta[1].max()

    # Show the data; click on the image for successive wavelength views
    if plot == True:
        extent = (xmin,xmax,ymin,ymax)
        norm = matplotlib.colors.Normalize(datacube.min(),datacube.max())
        for j in xrange(wave.size):
            p.clf()
            p.imshow(datacube[...,j],extent=extent,origin='lower',cmap=matplotlib.cm.rainbow,interpolation='none',norm=norm)
            cb = p.colorbar()
            p.title("View (wavelength) %d of %d" % ((j+1),wave.size))
            print "Click on the image repeatedly for successive wavelength views"
            p.waitforbuttonpress()

    # create interpolation object
    ip = ndiminterpolation.NdimInterpolation(datacube,theta)  # defaults are order=1 and mode='log'

    # example of usage: interpolate on another wave grid (mywave), with any combination of parameter values (vector)
    mywave = N.linspace(0.5,2.9,50)
    vector = [0.5,1]
    sed = ip(vector,mywave)   # the interpolated 'SED'

    # speedtest
    if number is not None:
        import timeit

        def speedtest():
            # generate a random vector from the support of theta (here uniform in all dimensions)
            vector = [(xmax-xmin) * N.random.random() + xmin, (ymax-ymin) * N.random.random() + ymin]
            sed = ip(vector,mywave)

        print "Benchmarking (%d interpolations)..." % number
        duration = timeit.timeit(speedtest,number=number)
        duration_per_call =  duration/float(number)
        print "Duration = %.2f seconds --> %.2e seconds per interpolation --> %d interpolations per second" % (number,duration_per_call,(1./duration_per_call))

    return ip, datacube, theta, mywave
