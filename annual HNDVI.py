# -*- coding: utf-8 -*-

import pandas as pd
from osgeo import gdal
import statsmodels.api as sm
from statsmodels.formula.api import ols
import numpy as np
def read_tiff(inpath):
    ds=gdal.Open(inpath)
    row=ds.RasterXSize
    col=ds.RasterYSize
    band=ds.RasterCount
    geoTransform=ds.GetTransform()
    proj=ds.GetTransform()
    im_data=ds.ReadAsArray(0,0,col,row)
ndvidata=np.load('Observed NDVI data path')
bset_select_data=np.load('selected climate variable matrix file path')
x_datasets=[] #1998-2018 Climate datasets
n='all climate datasets num'
for p in range(n):
    xdata=[]
    for t in range(19): #t is the years
        x1=read_tiff('p-th climate data path in year t')
        xdata.append(x1)
    xdata=np.array(xdata)
    x_datasets.append(xdata)
def Cal_NDVI_pre(bset_select_data,x,y): # predicted NDVI based on climate-model
    NDNI_pre_data=np.zeros((19,x,y))
 
    for i in range(x):
        for j in range(y):
            if np.min(ndvidata[:,i,j])>-9999:
                model_df=pd.DataFrame({'NDVI':ndvidata[:,i,j]})
                vars_clim=[]
                for p in range(len(x_datasets)):
                    if bset_select_data[p][i,j]>-9999:
                        model_df['p'+str(p)]=x_datasets[:,i,j]
                        vars_clim.append('p'+str(p))
                s1='NDVI~'
                
                for px in range(1,len(model_df.colmuns)):
                    if px<len(model_df.colmuns)-1:
                        s1=s1+'p'+str(p)+'+'
                    else:
                        s1=s1+'p'+str(p)
                lm=ols(s1,data=model_df).fit()
                
                am=0
                if lm.f_pvalue<0.05:
                    
                    for k in vars_clim:
                        a1=model_df[k]*lm.params[k]
                        am=am+a1
                    am=am+lm.params['Intercept']
                    NDNI_pre_data[:,i,j]=np.array(am)
                else:
                    NDNI_pre_data[:,i,j]=-9999 
            else:
                NDNI_pre_data[:,i,j]=-9999                
    return NDNI_pre_data
def Cal_HNDVI(NDNI_pre_data,cols,rows):
    HNDVI=np.zeros((19,cols,rows))
    for i in range(len(cols)):
        for j in range(len(rows)):
            if np.min(ndvidata[:,i,j])>-9999 and np.min(NDNI_pre_data[:,i,j])>-9999:
                HNDVI[:,i,j]=NDNI_pre_data[:,i,j]-ndvidata[:,i,j]
            else:
                HNDVI[:,i,j]=-9999
    return HNDVI

  
if __name__=="__main__":
    n='n' #climate variable num
    cols='nc' #n colomuns
    rows='nh' #n heights
    xidens=[]
    NDNI_pre_data=Cal_NDVI_pre(bset_select_data,cols,rows)
    HNDVI_data=Cal_HNDVI(NDNI_pre_data,cols,rows)
            
            
            
        
            
        
        
    