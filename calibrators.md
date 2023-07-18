# The Calibrator Object

## Overview
The goal of the `Calibrator` class is to convert a 1-D array of intensities to a calibration function with uncertainties. 
The `Calibrator` class serves as the parent for other Calibrators,
and implements the fitting, plotting, and saving of the calibration function. However, the `Calibrator` class itself does not find the (channel, wavelength) pairs from the spectra;
A subclass, such as `Distance_Calibrator` (Preferred) or `DFS_Calibrator` (Unfinished) must be used to actually identify the present lines.

## Distance Calibrator

### Theory
The distance calibrator objects works based on the assumption that the *distance between peaks* is the same across spectra of the same element.
Formally this means that if two lines have channel positions $x_{1A}$ and $x_{2A}$ in spectra A and positions $x_{1B}$ and $x_{2B}$ in channel B, then
$$x_{1A} - x_{2A} = x_{1B} - x_{2B}.$$

This observation allows us to create a distance file which stores the wavelengths and their uncertainties of lines we expect to see in a spectra,
as well as the distance between each line and some strong reference line. For example, the distance file for Neon spectra is shown below:

Wavelength|Wavelength Uncertainty| Channel Distance from 8.81 nm line.
---|----|----
6.73832|0.00012|-303.129488
7.5764|0.0004|-176.901644
8.80929|0.00014|0.0
9.7502|0.0004|128.5157
11.1136|0.0018|306.158035
11.6691|0.0005|375.204428
12.26404|0.00017|448.340851
12.7676|0.0007|508.29177
14.3314|0.0007|689.24213
14.7138|0.0007|732.171805
15.0101|0.0005|766.378538
17.6186|0.00028|1045.499954
19.5004|0.0008|1235.59335
23.3382|0.001|1636.177993
24.5404|0.00034|1763.212698
25.5352|0.0014|1870.635458

#### Note
Initially, these distances were obtained from a manual calibration. More precise distances and lines were obtained from the automatic calibration process.
Using this calibration, distance files for other spectra (such as background spectra) can be obtained by calibrating Neon files taken at the same time as the background. Manual tweaking may be required when adding lines to the distance file, but they stay relatively consistent.

### Algorithm
First, the centroids of the peaks are identfied using the `MultiPeakGaussian` class. Then, an anchor peak is chosen from the centroids, and assumed to be the reference peak from the distance file (the 8.81 nm line for neon). Using the channel distances in the distance file, we check to see if there are peaks where we expect them to be. If our anchor peak is at channel 800, for example, we would expect to see the 9.75 nm line at channel 800 + 128.5, the 11.11 nm line at 800 + 306.2 channels, and so on. If we have a peak within some small tolerance (typically 2 channels), we "identify" it as a match.

The issue is that the first guess for the anchor peak may not have been correct. To remedy this, we iterate overall peaks in the spectra, picking them as the anchor line, and seeing how many peaks line up with the distance file. The anchor peak will be the line with the most matches!

Once the line have been identified, the `Distance_Calibrator` object will store the information in the `.solution_arr` attribute for use by the standard `Calibrator` functions.

### Usage / Example

The Distance_Calibrator object has two required arguments: arr, the y-data of the spectra and element, two - three letter string that specifies the spectra's state.

```python
from euv_fitting.calibrate.calibrators import Distance_Calibrator

D = Distance_Calibrator(arr = img, element = 'Ne', num_peaks = 30)
#This may take a second as the multipeakgaussian fits the data
D.calibrate() #peak identification step
```

Now that the peaks have been matched with their wavelengths, we can find the calibration function:

```python
D.fit(verbose = True, cinterval = 99.95)
D.print_info()
D.plot()
D.residual_plot()
```

Note that `D.fit` takes care of any outliers in the data at a `cinterval` confidence interval. 

By default, all plots display automatically. To adjust the plots or to save them, use:

```python
import matplotlib.pyplot as plt
f = Figure()
ax = plt.gca()
D.plot(ax = ax)
plt.savefig('example.png')
```

Sometimes one spectra alone may not provide good coverage over the entire wavelength region. To combine spectra, calibrate them individually, and then use the `D.join()` method to combine the lines that were found.

```python
D2 = Distance_Calibrator(arr = bkg_img, element = 'Ba', num_peaks = 25)
D2.calibrate()
D.join([D2])

D.fit(verbose = True)
D.plot()
D.residual_plot()
```

### Advanced Arguments

When you call the `Distance_Calibrator` object, you can pass in arguments to `MultiPeakGaussian.fit()` to adjust the fitting process. For example, `xs` and `function` are arguments for both function. The `gauss_locs` argument is a list of x-positions where you want to manually add gaussians. The `timeout` argument is a number in seconds for how long the calibrator should try to fit the data before throwing an error.









