# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 20:02:27 2019

@author: akshay
"""

import sqlite3 as lite
from mzi_device import MZIDevice

def connect(sqliteFile):
    conn = lite.connect(sqliteFile, check_same_thread=False)
    print("Connection Opened to: " + sqliteFile)
    return conn

def close(conn):
    conn.close()
    
def createTable(conn, cursor):
    with conn:
        cursor.execute("""CREATE TABLE MZI_DEVICE(
            n1 FLOAT,
            n2 FLOAT,
            n3 FLOAT,
            alpha FLOAT,
            delta FLOAT,
            fsr FLOAT,
            mean_ng FLOAT)""")
        
        
def insertDevice(conn, cursor, device):
    print("Device parameters: %f %f %f %f %f %f %f" %(device.n1, device.n2, device.n3, device.alpha, device.deltaLength, device.fsr, device.meanGroupIndex))
    with conn:
        cursor.execute("INSERT INTO MZI_DEVICE VALUES (:n1, :n2, :n3, :alpha, :delta, :fsr, :mean_ng)", {'n1':device.n1, 'n2':device.n2, 'n3':device.n3, 'alpha':device.alpha, 'delta':device.deltaLength, 'fsr':device.fsr, 'mean_ng':device.meanGroupIndex})
        
        
def selectDevice(conn, cursor, device):
    cursor.execute("SELECT id FROM MZI_DEVICE WHERE n1=:n1 AND n2=:n2 AND n3=:n3 AND alpha=:alpha AND delta=:delta AND fsr=:fsr AND mean_ng=:mean_ng)", {'n1':device.n1, 'n2':device.n2, 'n3':device.n3, 'alpha':device.alpha, 'delta':device.deltaLength, 'fsr':device.fsr, 'mean_ng':device.meanGroupIndex})
 
    
def dropTable(conn, cursor):
    with conn:
        cursor.execute("DROP TABLE MZI_DEVICE")
    
if __name__=="__main__":
    try:
        conn = connect(r'D:\Courses\Edx_SiliconPhotonics\Phot1x_DataAnalysis-Python\Phot1x_DataAnalysis-Python\mzi_device.db')
        c = conn.cursor()
        createTable(conn,c)
       # dropTable(conn,c)
    except lite.Error:
        if conn:
            conn.rollback()
    
    finally:
        if conn:
            conn.close()
    
