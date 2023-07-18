#!/usr/bin/env python
# coding: utf-8

# In[1]:


from euv_fitting.calibrate.utils import SpeReader

S = SpeReader('../euv_fitting/calibrate/270.spe')
img = S.load_img()

print(f'Spectra has shape {img.shape}')
print('With metadata:')
S.print_metadata()


# In[2]:


import matplotlib.pyplot as plt

plt.plot(img.T)
plt.xlabel('Channel Number [-]')
plt.ylabel('Intensity [ADU]')
plt.title('Neon Spectra')

plt.legend([f'Frame {i + 1}' for i in range(img.shape[0])])
plt.show()


# In[3]:


plt.plot(img.T)
plt.xlabel('Channel Number [-]')
plt.ylabel('Intensity [ADU]')
plt.title('Neon Spectra')

plt.legend([f'Frame {i + 1}' for i in range(img.shape[0])])

plt.arrow(660, 1800, 0, -400, width = 30, color = 'orange')
plt.text(200, 2000, 'Cosmic Ray in Frame 2')
plt.show()


# In[4]:


from euv_fitting.calibrate.utils import CosmicRayFilter

CRF = CosmicRayFilter()
img_filtered = CRF.apply(img)

plt.plot(img_filtered)
plt.xlabel('Channel Number [-]')
plt.ylabel('Intensity [ADU]')
plt.title('Filtered Neon Spectra')
plt.show()


# In[5]:


from euv_fitting.calibrate.calibrators import Distance_Calibrator

Ne_Cal = Distance_Calibrator(img_filtered, 'Ne', num_peaks = 25)


# In[6]:


Ne_Cal.multi.plot_fit()
print('Printing information for the 6th peak fit.')
print(Ne_Cal.multi.gauss_data[5, :, :])


# In[7]:


Ne_Cal.calibrate()
Ne_Cal.fit()
Ne_Cal.plot()
Ne_Cal.print_info()


# In[8]:


Ne_Cal.residual_plot()

