# EUV Fitting Introduction

This will be an introduction to what euv_fitting can do, important options that are available, and how to automate key parts of the analysis process.

--

## A typical analysis project with this package goes as follows:



0. Import all neccesary classes
```python
import pandas as pd
from euv_fitting.calibrate.calibrators import Distance_Calibrator
from euv_fitting.calibrate.utils import SpeReader, CosmicRayFilter
```
1. The spectra is loaded either from a .spe file or the EUV.h5 database

```python
S = SpeReader('./data/numbered/270.spe')
img = S.loadimg()

#The various metadata in the .spe file can be accessed through the metadata attribute class.
print(S.metadata['rawtime'])
```
2. A cosmic ray filter is applied to remove meaningless peaks
```python
C = ComsicRayFilter(filtervalue = 5)
img = C.apply()
```

3. A Distance_Calibrator object is created that fits gaussians to the peaks
```python
#The distance file you use depends on the elements present in the spectra
#Here NO_distances is used as both neon and oxygen are in the spectra
D = Distance_Calibrator(img, distance_file = 'NO_distances.csv',
        \ num_peaks = 30)
```
##### This may take a second as it fits the data with gaussians.

4. Peaks are assigned wavelength through analysis of the distances between peaks
```python
#For more information about what this actually does, see the source code or the explanation in writeup.pdf (TO DO)
D.calibrate()
```
5. The identified (channel, wavelength) pairs are used to fit a third order polynomial
```python
D.fit(verbose = True)
D.plot()
D.residual_plot()
```

And there we go! At this point the parameters of the fit can be collected and exported however you wish. For example:
```python
popt, pcov = D.popt, D.pcov #popt are the coefficients of the third order polynomial
                            #while pcov is the covariance matrix of the fit
channels = D.xs
wavelengths = D.f3(channels, *D.popt) #Applies the calibration function to the channels
confidence_bands95 = D.confidence_bands(cinterval = 95)
data = np.vstack([channels, wavelengths, confidence_bands95])
df = pd.DataFrame(data, columns = ['ch', 'wl','conf_band95'])
df.to_csv('example.csv')
```
