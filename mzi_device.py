# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 18:47:46 2019

@author: akshay
"""
from numpy import *

class MZIDevice(object):
    
    def __init__(self, n1, n2, n3, alpha, deltaLength, fsr, ng):
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        self.alpha = alpha
        self.deltaLength = deltaLength
        self.fsr = fsr
        self.ng = ng
        
   
    @property     
    def meanGroupIndex(self):
        groupIndex = self.ng
        return mean(groupIndex)