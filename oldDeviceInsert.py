# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 15:12:18 2019

@author: aksha
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 21:58:48 2019

@author: akshay
"""


from queue import Queue
import threading
import time
from scipy.io import loadmat
from numpy import *
import autocorrResult as autoCorrelate
from mzi_device import MZIDevice
import sqlite_mzi_helper


dataFileList = ['ZiheGao_MZI8_266_Scan1.mat',\
                'ZiheGao_MZI17_265_Scan1.mat']
dataFilePath="DataSet1/"

dbFile='D:\\Courses\Edx_SiliconPhotonics\Phot1x_DataAnalysis-Python\Phot1x_DataAnalysis-Python\mzi_device.db'
        
        
                
def insertCall(conn, insertQueue):
    while True:
        c = conn.cursor()
        deviceId, device = insertQueue.get()
        print ("Adding Device: " + deviceId)
        sqlite_mzi_helper.insertDevice(conn,c,device)
        c.close()
        insertQueue.task_done()
            

def putInsertQueue(insertQueue, deviceId, device):
    name = threading.currentThread().getName()
    print ("Thread: " + name)
    print ("Putting device: " + deviceId)
    insertQueue.put((deviceId, device))
    

    
if __name__ == "__main__":

    conn = sqlite_mzi_helper.connect(dbFile)
    insertQueue = Queue()
    
    for devData in dataFileList:
        #Loading matlab data and getting device object after parameter extraction
        matData= loadmat(dataFilePath+devData, squeeze_me=True, struct_as_record=False)
        wavelength = matData['scanResults'][0].Data[:,0]/1e9
        power = matData['scanResults'][0].Data[:,1]
        
        deviceId, device = autoCorrelate.performAutocorr(devData,wavelength,power)

        t = threading.Thread(name="Producer Thread - "+deviceId, target=putInsertQueue, args=(insertQueue, deviceId, device), daemon=True)
        t.start()
    
    try:
       t = threading.Thread(name="Consumer Thread", target=insertCall, args=(conn, insertQueue), daemon=True)
       t.start()
    except:
        if conn:
            print("Rolling Back")
            conn.rollback()
       
    
    
    insertQueue.join()
    print("Closing Connection")
    sqlite_mzi_helper.close(conn)
