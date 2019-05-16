# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 21:58:48 2019

@author: akshay
"""


from scipy.io import loadmat
from numpy import *
import autocorrResult
from mzi_device import MZIDevice
import sqlite_mzi_helper
import time

dataFilePath="DataSet1/"

dataFileList = ['ZiheGao_MZI8_266_Scan1.mat',\
                'ZiheGao_MZI17_265_Scan1.mat']

dbFile='D:\\Courses\Edx_SiliconPhotonics\Phot1x_DataAnalysis-Python\Phot1x_DataAnalysis-Python\mzi_device.db'

startTime= time.time()

for data in dataFileList:
    matData= loadmat(dataFilePath+data, squeeze_me=True, struct_as_record=False)
    wavelength = matData['scanResults'][0].Data[:,0]/1e9
    power = matData['scanResults'][0].Data[:,1]
    deviceName, device = autocorrResult.performAutocorr('ZiheGao_MZI3_270_Scan1.mat',wavelength,power)

endTime= time.time()

print("Processing Time:")
print(endTime-startTime)

#try:
#    conn = sqlite_mzi_helper.connect(r'D:\Courses\Edx_SiliconPhotonics\Phot1x_DataAnalysis-Python\Phot1x_DataAnalysis-Python\mzi_device.db')
#    c = conn.cursor()
#    sqlite_mzi_helper.insertDevice(conn,c,device)
#except:
#    if conn:
#       conn.rollback()

#finally:
#    if conn:
#        sqlite_mzi_helper.close(conn)
