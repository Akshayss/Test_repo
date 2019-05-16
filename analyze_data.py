# by Mike Caverley, Lukas Chrostowski, 2014-2015
# Curve fitting of MZI spectra
# Step 1 - get the approx FSR from the spectrum using autocorrelation
# Step 2 - use this as an input for the curve fitting routine

from scipy.io import loadmat
from numpy import *
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import re
import os

# for autocorr:
from matplotlib.mlab import find
from scipy.signal import fftconvolve
from parabolic import parabolic


coordFile = 'DataSet1/EB486A_URChip3Coords1.txt'

with open(coordFile) as f:
    fileData = f.readlines()

deviceLengthDict = {}

for line in fileData[1:-1]:
    splitLine = line.strip().split(',')
    deviceLengthDict[splitLine[5]] = float(splitLine[6])

matEnvelopeData = loadmat('DataSet1/ZiheGao_MZI1_272_Scan1.mat', squeeze_me=True, struct_as_record=False)
envelopeWavelength = matEnvelopeData['scanResults'][0].Data[:,0]/1e9
envelopePower = matEnvelopeData['scanResults'][0].Data[:,1]

dataFileNameList = [ 'LukasChrostowski_MZI2_136_Scan1.mat', \
                'ZiheGao_MZI2_271_Scan1.mat', 'ZiheGao_MZI3_270_Scan1.mat', 'ZiheGao_MZI4_269_Scan1.mat',\
                'ZiheGao_MZI5_268_Scan1.mat', 'ZiheGao_MZI6_267_Scan1.mat', 'ZiheGao_MZI8_266_Scan1.mat',\
                'ZiheGao_MZI17_265_Scan1.mat']

#dataFileNameList = [ 'ZiheGao_MZI2_271_Scan1.mat']
x0 = array([ 2.40, -1.13, -0.32,  1000])

               

for dataFile in dataFileNameList:
    
    matData = loadmat('DataSet1/'+dataFile, squeeze_me=True, struct_as_record=False)
    p = re.compile('(.*)_[0-9]+_Scan1.mat')
    deviceName = p.findall(dataFile)[0]
    
    wavelength = matData['scanResults'][0].Data[:,0]/1e9
    power = matData['scanResults'][0].Data[:,1]
    powerNormalized = power-envelopePower
    powerLinear = 10**(powerNormalized/10)
    
        
    def wavelength_from_autocorr(signal, sampling):
        """Estimate wavelength using autocorrelation
        
        from https://gist.github.com/endolith/255291
        
        Pros: Best method for finding the true fundamental of any repeating wave, 
        even with strong harmonics or completely missing fundamental
        
        Cons: Not as accurate, doesn't work for inharmonic things like musical 
        instruments, this implementation has trouble with finding the true peak
        
        """
        # Calculate autocorrelation (same thing as convolution, but with one input
        # reversed in time), and throw away the negative lags
        signal -= mean(signal) # Remove DC offset
        corr = fftconvolve(signal, signal[::-1], mode='full')
        corr = corr[len(corr)/2:]
                
        # Find the first low point
        d = diff(corr)
        start = find(d > 0)[0]
        
        # Find the next peak after the low point (other than 0 lag).  This bit is 
        # not reliable for long signals, due to the desired peak occurring between 
        # samples, and other peaks appearing higher.
        i_peak = argmax(corr[start:]) + start
        i_interp = parabolic(corr, i_peak)[0]
        print "i_interp: %f" %i_interp
                
        return i_interp * sampling

    fsr=wavelength_from_autocorr(powerLinear, 1e-12)
    print 'fsr: %f [nm]' %(fsr*1e9)

    def neffFuncFit(wavelenegth, n1, n2, n3):
        return n1 + n2*(wavelength-mean(wavelength))*1e6+n3*(wavelength-mean(wavelength))**2*1e12
        
    L = deviceLengthDict[deviceName]*1e-6
        
    def curveFitFunc(wavelength, n1, n2, n3, alpha):   
        L1=0
        L2=L
        neff=neffFuncFit(wavelength, n1, n2, n3)
        beta = 2*pi*neff/wavelength
        return 10*log10(0.25*abs(exp(-1j*beta*L1-alpha/2*L1)+exp(-1j*beta*L2-alpha/2*L2) )**2)
    
    popt, pcov = curve_fit(curveFitFunc, wavelength, powerNormalized, p0=x0, maxfev=1000)
    print "perr: %f" % sum(pcov)
    
    neffFit = neffFuncFit(wavelength, popt[0], popt[1], popt[2]) 
    ng = neffFit[:-1]-wavelength[:-1]*diff(neffFit)/diff(wavelength)

    saveFigFileName = os.path.splitext(dataFile)[0]+'.pdf'    
    
    plt.figure()
    plt.plot(wavelength*1e9, powerNormalized)
    plt.plot(wavelength*1e9, curveFitFunc(wavelength, popt[0], popt[1], popt[2], popt[3]))
#    plt.plot(wavelength[peakind]*1e9, powerNormalized[peakind], 'bo')
    plt.xlim((1530,1560))
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Transmission (dB)')
    plt.title('%s\nng: %f L: %g $\mathrm{\mathsf{\mu m}}$'%(dataFile,mean(ng),L*1e6))
    plt.savefig(saveFigFileName)
    plt.show()

    saveFigFileName = os.path.splitext(dataFile)[0]+'_ng.pdf' 
    
    plt.figure()
    plt.plot(wavelength[:-1]*1e9, ng)
    plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Group index')
    plt.title('%s'%dataFile)
    plt.savefig(saveFigFileName)
    plt.show()

