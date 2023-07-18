Euv_fitting: Automated Peak Fitting and Calibration of NIST EUV Spectra
=======================================================================

.. _lmfit: https://lmfit.github.io/lmfit-py/index.html

Euv_fitting provides a high level interface for processing NIST Extreme Ultraviolet (EUV)
Spectra. It is written entirely in Python, and contains classes for opening,
processing, and plotting spectra from the NIST EUV Spectrometer. Euv_fitting relies
heavily on `lmfit`_, and has functionality including:

  * Processing of binary .SPE files into NumPy arrays and metadata via
    :class:`~euv_fitting.calibrate.utils.SpeReader` objects. The cosmic rays present in these
    files can then be removed using a :class:`~euv_fitting.calibrate.utils.CosmicRayFilter` object.

  * A searchable hdf5 database of the last ten years of NIST EUV spectra. Users can filter
    their search for specific elements, dates, and beam energies through the
    :class:`~euv_fitting.euvh5.euvh5_handler.EUVH5_Handler` class.

  * Using :class:`~euv_fitting.calibrate.utils.MultiBatchGaussian` objects
    to automatically detect peaks in a spectra and fit them with gaussians. The fit
    data is easily accessible in NumPy arrays, and users can adjust the number
    of detected peaks and manually input peak locations that are missed.

  * Identification of calibration lines using :class:`~euv_fitting.calibrate.calibrators.Distance_Calibrator`
    objects. Distance_Calibrators can also convert collections of identified calibration lines
    into the calibration coefficients and their uncertainties. Systematic
    uncertainties present in the spectra are also estimated via the reduced chi-squared.

  * Iterative intensity calibration of EUV spectra based on Poisson statistics
    and the response function of the CCD camera.




.. toctree::
   :maxdepth: 2
   :caption: Contents

   intro
   peakfitting
   calibration


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
