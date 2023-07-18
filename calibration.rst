.. _calibration_Chapter:

=========================
Calibrators
=========================

Calibration Process
===================

Uncertainty Analysis, Intensity Calibration, Etc.


Calibrator
==========

Includes general calibration functionality such as uncertainty analysis,
intensity calibration, printing, and plotting.

.. autoclass:: euv_fitting.calibrate.calibrators.Calibrator
   :members:

Distance Calibrator
===================

Child class of :Calibrator:, identifies calibration lines based on their relative distances.

.. autoclass:: euv_fitting.calibrate.calibrators.Distance_Calibrator
   :members:
