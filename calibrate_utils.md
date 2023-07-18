# Overview

The module `euv_fitting.calibrate.utils` contains three key classes for NIST spectral analysis. `SpeReader`, which loads data from .spe files, `CosmicRayFilter`, which removes cosmic rays from spectra, and `MultiPeakGaussian` which extracts peak information from a spectra. This file serves as an explanation for what they do and how they relate to the analysis process.

## `SpeReader`

### What is a .spe file?

SSPS is a file format developed by IBM for easy statistical analysis. Any file of the form "file_name.spe" has two main parts:
1. A header of 4100 bits containing metadata like the size of the stored array, the time it was taken, and the gain of the ADC conversion.
2. The data itself, also stored in binary. Each .spe file is typically split into 5 sections, or 'frames', of 2048 element arrays.


To get started, create an instance of the SpeReader class, passing in the .spe file location as an argument.

```python
from euv_fitting.calibrate.utils import SpeReader
S = SpeReader('example.spe')
```

This loads the size of the data array and all metadata it can find. The metadata is stored as a dictionary in `S.metadata`, and can be accessed using standard dictionary notation. If you want to see all available metadata, use the .print_metadata() method.

```python
time = S.metadata['rawtime']
gain = S.metadata['gain']

S.print_metadata()
```

Finally, extract the spectra from the .spe file using .load_img(). This returns a numpy array of all the data it can find, typically a 5 x 2048 array.
```python
img = S.load_img()
```

## `CosmicRayFilter`

### What are cosmic rays, and how do they affect the data?

Cosmic rays are high energy photons originating from outside the experiment environment. They typically dwarf all other features in the spectra, and affect only one channel. To remove them, the different frames in a .spe file are compared and checked for outliers from the expected poisson noise distribution. For any channel, if one frame has a value grossly different from the other frames, it is flagged as a cosmic ray and replaced with the mean of the values in the other frames.

To remove them, first create an instance of the `CosmicRayFilter` class. The argument filterval controls how many standard deviations from the mean a value can be before it is flagged as a cosmic ray. Five is a typical value, with higher being more strict and 0 being the minimum.

```python
from euv_fitting.calibrate.utils import CosmicRayFilter
C = CosmicRayFilter(filterval = 5)
```

Then pass the 5 x 2048 array through the filter to get your final array. By default, CosmicRayFilter averages the 5 2048 element arrays into one 2048 element array after filtering. To toggle this, set combine = False. This can be useful if one frame of your spectra is obviously degraded.

```python
img = C.apply(img) #img.shape = (2048,)

#OR
img = C.apply(img, combine = False) #img.shape = (5, 2048)
img = img[0] #Take the first frame to get a good image.
```

## `MultiPeakGaussian`

### Motivation
The final steps of spectral analysis is to make predictions based off the gaussian peaks in the data. Each peak corresponds to its own energy transistion, so any analysis must be able to extract data about those peaks: Their center, width, amplitude, and the uncertainty in those parameters. If each peak were cleanly separated, they could be modelled and fit individually. However, it is typical to have several peaks in the same region, and ignoring that can lead to systematic shifts in the data.

### Method
To address the interference of peaks, ```MultiPeakGaussian``` analyzes the whole spectra simulatenously. The function relating channel (x) to intensity(y) is:

$$y = a + bx + cx^2 + dx^3 + \sum_{i=0}^{N-1}\frac{Amp_i}{\sigma_i\sqrt{2\pi}}e^{-(x-\mu_i)^2/(2\sigma_i^2)}$$

Where a, b, c, and d are the coefficients of the background, N is the number of gaussians, $Amp_i$ is the amplitude of gaussian i, $\mu_i$ is the center of gaussian i, and $\sigma_i$ is the sigma (parameter related to the width) of gaussian i.

The `MultiPeakGaussian` class automatically finds these peaks, compiles them into an lmfit model, and fits the data to return the correct parameters.

#### Note for developers:
If you are familiar with gaussian like functions, you know that after 4 or 5 sigma the gaussian drops off to essentially 0. At some point, the developers aim to reduce runtime by setting the gaussian to 0 far enough away from the center.

### Usage
Create a MultiPeakGaussian object, passing in the y values and number of peaks you would to fit.

```python
from euv_fitting.calibrate.utils import MultiPeakGaussian
multi = MultiPeakGaussian(arr = img, num_peaks = 30)

# By default, MultiPeakGaussian sets the x-axis to just be [0, 1, ..., len(arr) - 1]
# If you would like to set the x-axis, use the xs argument.

# multi = MultiPeakGaussian(arr = img, xs = your_x_arr, num_peaks = 30)
```

From here, calling `multi.fit()` will go through the fitting process. To verify that the fit has gone well, call `multi.plot_fit()` to show the original data and the best-fit on the same graph.

```python
multi.fit()
multi.plot_fit()

popt = multi.popt #parameters of best fit
pcov = multi.pcov #covariance matrix of fit
centroids = multi.centroids # N element list of [[center1, uncertainty_in_center1],
                            #          [center2, uncertainty_in_center2], ...]
gauss_data = multi.gauss_data 
#each row is [[center, uncertainty], [amplitude, uncertainty], [sigma, uncertainty]]
for row in gauss_data:
  print(row)
```

### Advanced - Peak Detection

The automatic peak detection works by looking for 3 consecutive points going up and 2 consecutive points going down. If the data is particularly noisy or spiky, that method may fail.
To remedy this, there are two options:

1.) Call ```multi.add_gaussian(x_pos_of_peak)``` to manually force a peak at that location.
2.) Increase the smoothing factor in ```.get_peak_indices```, currently only available through code tweaking.
 
### Advanced - `multi.fit()` arguments

function: Several applications are better fit by a voigt function rather than a gaussian. To switch between the two, use `multi.fit(function = 'voight')`. Currently, only 'gaussian' and 'voigt' are supported.

same_sigma: By default, the sigmas of all the gaussians can vary independently. If you would like to fix them to be the same, use `multi.fit(same_sigma = True)`

### Advanced - Composite features

For the TES precision calibrations the composition of complex features are sometimes known: for example, you may know that a peak around 500 eV is actually composed of three peaks at 499.9 eV, 500.1 eV, and 500.3 eV, with the 500.1 eV and 500.3 eV peaks having a 3:1 ratio in intensities.

To fit this peak with a composite of gaussians rather than a single gaussian, you can use the following code:

```python
multi = MultiPeakGaussian(img, xs = x, num_peaks = 10)
multi.add_composite(lit_vals = [499.9, 500.1, 500.3], \
                    rel_intensities = [None, (2,3), None])
multi.fit()
```

This sets 3 gaussians in the 500 eV region, with the property that the 1st index (500.1 eV) peak must have 3 times the amplitude of the second peak. If a entry in relative intensities is set as None, that means that peaks amplitude is a free parameter of the fit.

Equivalently, you could set rel_intensities = [None, None, (1, 1/3)]






