
from scipy.io import loadmat
from numpy import *
import matplotlib.pyplot as plt
import os


FileName = 'ZiheGao_MZI2_271_Scan1.mat'
matData = loadmat(FileName, squeeze_me=True, struct_as_record=False)
    
wavelength = matData['scanResults'][0].Data[:,0]/1e9
power = matData['scanResults'][0].Data[:,1]
        
saveFigFileName = os.path.splitext(FileName)[0]+'.pdf'
plt.figure()
plt.plot(wavelength*1e9, power)
plt.xlim((1530,1560))
plt.xlabel('Wavelength (nm)')
plt.ylabel('Transmission (dB)')
plt.title('%s'%(saveFigFileName))
plt.savefig(saveFigFileName)
plt.show()
