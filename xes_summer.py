# -*- coding: utf-8 -*-
"""
Code for the sum of raw XES-V2C data in windows

Use info: xes_summer([Scan_N1 Scan_N2 ...], Energy,FF,I1, method) 

-> Sum of column FF of the datafile ScanNx according to "method"

Indication of the method is optional.
Sums the scans up using one of the two methods:
  method = 1    uses the statistical accuracy as a weight
  method = 2    "raw" summing, error=sqrt(sum(ys))
"""
import numpy as np
import subprocess
import os
import matplotlib.pyplot as plt
from sys import platform


def xes_summer(files_to_sum, colx, coly, colI1, *args):
    varargin = args
    nargin = 4 + len(varargin)
    if np.size(files_to_sum)==1:
        print('Warning! Nothing to sum here; did you give me the right scan numbers?')
    
    colx=colx-1; coly=coly-1; colI1=colI1-1; 
    files_in_dir=[]; 
    if platform == "linux" or platform == "linux2":
        for r, d, f in os.walk(os.getcwd()):
            for indexf in range(0,len(files_to_sum)):
                for item in f:
                    if files_to_sum[indexf] in item:
                        files_in_dir.append(item)
    elif platform == "win32":
        # r=>root, d=>directories, f=>files
        for r, d, f in os.walk(os.getcwd()):
            for indexf in range(0,len(files_to_sum)):
                for item in f:
                    if files_to_sum[indexf] in item:
                        files_in_dir.append(item)

    data= np.loadtxt(files_in_dir[0])
    ffI1=np.ones((np.ma.size(data,0),len(files_to_sum))); 
    errI1=np.ones((np.ma.size(data,0),len(files_to_sum)));  
    energy=np.ones((np.ma.size(data,0),len(files_to_sum))); 
    
    for indarr in range(0,len(files_in_dir)):
        data= np.loadtxt(files_in_dir[indarr])
        energy[:,indarr]=data[:,colx]; 
        ffI1[:,indarr] = data[:,coly] / data[:,colI1];
        errI1[:,indarr] = np.sqrt(data[:,coly]) / data[:,colI1];
    

    if nargin<=4: 
        method=1
####################################################        
    if method==1:
        if np.ma.size(ffI1,1)>1:
            ys=np.sum((ffI1/(errI1**2)),axis=1) / (np.sum(1/(errI1**2),axis=1));
            yse=np.sqrt(1/np.sum(errI1**2,axis=1));
        else:
            ys=ffI1; yse=errI1;
        
        
    if method==2:
        if np.ma.size(ffI1,1)>1:
            ys=np.sum(ffI1,axis=1); yse=np.sqrt(ys);
        else:
            ys=ffI1; yse=errI1;        
        
########################################################################        
    fig = plt.figure()
    plt.plot(energy, ffI1)
    plt.errorbar(energy[:,1], ys, yse, color='black',linewidth=2)             

    TITLE="".format(len(Xsel))
    plt.title(TITLE)
    plt.xlabel('Energy (eV.)'); plt.ylabel('Intensity (Arb. Units)');
    #plt.legend()
    plt.show()   
    
########################################################################        
#if method==1, 
#  ye(find(ye==0))=1;
#  if size(y,2)>1, 
#    ys=sum(y'./ye'.^2)./(sum(1./ye'.^2)); ys=ys';
#    yse=sqrt(1./sum(1./ye'.^2)); yse=yse';
#  else
#    ys=y; yse=ye;
#  end
#end
#if method==2,
#  if size(y,2)>1,
#    ys=sum(ys')'; 
#    yse=sqrt(ys);
#  else
#    ys=y; yse=ye;
#  end
#end       
