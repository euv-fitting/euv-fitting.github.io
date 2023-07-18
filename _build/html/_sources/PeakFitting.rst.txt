.. _peakfitting_Chapter:



=================================
Peak Fitters
=================================

In order to complete calibration and line identification, it is essential to know
the center of the peaks in a spectra. To this end, euv_fitting include automatic
peak fitting classes that will extract these centers.

Introduction to Peak Fitting
============================

Peak fitting has three main steps:

1. Detection of peaks in the spectra
2. Determination of region to fit for each peak
3. Least Squares minimization of gaussian parameters.

Both MultiBatchGaussian and MultiPeakGaussian represent peaks as gaussian distributions, or

.. math::
  I(x; A, x_0, \sigma) = \frac{A}{\sigma \sqrt{2 \pi}} \exp(\frac{-(x-x_0)^2}{2 \sigma ^ 2})

Where :math:`x` is the channel or wavelength, :math:`I(x)` is the intensity at a
given x value, :math:`A` is the amplitude, :math:`x_0` is the center
of the gaussian, and :math:`\sigma` controls the width. The children of the PeakFitter
class convert arrays of x, y data into the best-fit parameters of the gaussians
in the data.

As an example on some dummy data:

.. jupyter-execute::

    import numpy as np
    import matplotlib.pyplot as plt

    from euv_fitting.calibrate.utils import MultiBatchGaussian

    def gauss(x, amp, cen, sig):
      return amp / (sig * np.sqrt(2 * np.pi)) * np.exp(-(x - cen) ** 2 / (2 * sig ** 2))

    x = np.linspace(0, 2047, 2048)

    N_GAUSS = 10
    AMPLITUDES = 1000 + np.random.random(size = N_GAUSS) * 500
    CENTERS = np.linspace(300, 1800, N_GAUSS)
    SIGMAS = np.minimum(2 + np.random.normal(0, 0.5, size = N_GAUSS), 1)

    y = sum(gauss(x, amp, cen, sig) for amp, cen, sig in zip(AMPLITUDES, CENTERS, SIGMAS)) #Add amplitudes of each gaussian
    y += np.random.normal(400, 10, size = 2048) #Add random gaussian noise

    multi = MultiBatchGaussian(y, x, num_peaks = N_GAUSS)
    #Note the x argument is optional. If not given, x defaults to np.linspace(0, len(y) - 1, len(y))

    multi.fit()
    multi.plot_fit(normalize_background = False)

.. jupyter-execute::

    f, ax = plt.subplots() #Generate ax object for multi.plot_fit()
    multi.plot_fit(ax = ax, normalize_background = False)
    ax.set_xlim([275, 325])
    plt.show()

The centroids are stored in the `multi.centroids` attribute, and information about
all of the peak parameters are stored in the `multi.gauss_data` attribute.

.centroids is an (N x 2) NumPy array, where the first column is the center value and
the second is the center uncertainty. By default, `.centroids` is sorted in decreasing
order of intensity. The `.get_centroids_ascending()` method returns centroids in increasing
order of center value.

.. jupyter-execute::

    best_fit_centers, best_fit_uncertainties = multi.get_centroids_ascending().T

    #Print column headers
    print(f"{'True Center':>14}, {'Fit Center':>14}, {'Fit Center Uncertainty':>20}")

    for true_center, best_fit_center, best_fit_uncertainty in zip(
        CENTERS, best_fit_centers, best_fit_uncertainties):



      print(f'{true_center:14.3f}, {best_fit_center: 14.3f}, {best_fit_uncertainty: 20.3f}')


.. jupyter-execute::
    :hide-code:

    plt.errorbar(CENTERS, CENTERS - best_fit_centers,
                  yerr = best_fit_uncertainties, fmt = '^b', label = '1 Sigma Error Bar')
    plt.xlabel('True Centroid [-]')
    plt.ylabel('Residual [-]')
    plt.legend()
    plt.show()

The centroids can then be used by the calibration classes or analyzed further
for line identification.

Read on for more information about the two peak fitting classes, or continue to
the next page to learn about the calibration process.





MultiBatchGaussian
==================

MultiBatchGaussian leverages the fast drop-off of the gaussian function to
reduce runtime by fitting isolated gaussians separately. If several gaussians are close
enough to affect each other (within ~12 channels) they are grouped into a **batch**.
Each batch of gaussians is then fit with the appropriate number of gaussians, as well
as a constant or linear background.

.. autoclass:: euv_fitting.calibrate.utils.MultiBatchGaussian
   :members:

MultiPeakGaussian
=================

  MultiPeakGaussian fits the entire spectrum simultaneously, and is similar to treating
  the whole spectra as one large batch. This has the benefit of not needing an initial
  guess of the gaussian's :math:`\sigma`, but does substantially increase the runtime/
  instability of the fitting process.

.. autoclass:: euv_fitting.calibrate.utils.MultiPeakGaussian
   :members:
