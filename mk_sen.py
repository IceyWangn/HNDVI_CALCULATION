# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 16:28:02 2019

@author: Administrator
"""

import numpy as np
import math

def calszc(x1):
    s=0
    length=len(x1)
    
    for m in range(0,length-1):
        
        for n in range(m+1,length):
            
            if x1[n]>x1[m]:
                s=s+1
            elif x1[n]==x1[m]:
                s=s+0
            else:
                s=s-1
    vars=length*(length-1)*(2*length+5)/18
    #计算zc
    if s>0:
        zc=(s-1)/math.sqrt(vars)
    elif s==0:
        zc=0
    else:
        zc=(s+1)/math.sqrt(vars)
           
    zc1=abs(zc)
        
    ndash=length*(length-1)/2
    slope1=np.zeros(int(ndash))
    m=0
    for k in range(0,length-1):
        for j  in range(k+1,length):
            slope1[m]=(x1[j]-x1[k])/(j-k)
            m=m+1
            
    slope=np.median(slope1)
    return slope,zc1

if __name__=="__main__":
    
    Y_HNDVI=np.load('HNDVI data File path')
    slope1,z_value=calszc(Y_HNDVI)#obtained the z-value and slope value of HNDVI time series