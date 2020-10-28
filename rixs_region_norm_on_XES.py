"""
Script for RIXS-regions measured in different sample-positions with XES reference measurement
XES normalisation necessary to account sample-inhomogeneity in amount of scattering atomic fraction

"""

import numpy as np
import matplotlib.pyplot as plt
import os
import csv

###############################################################################
# Edit scan number and output name! 
XES_norm=[143287, 143292, 143295, 143298, 143302];
RIXS_area=[143290, 143293, 143296, 143299, 143300]; 
col_e_mono=0; # Col. indexes for energy of monochromator (XAS), Spectrometer (XES), and Intensity Norm. over beam intensity  
col_e_XES=1;
col_ffi0=5;
OUT_NAME='Normalised_RIXS.dat';
###############################################################################
gate='allow';


if len(RIXS_area) != len(XES_norm):
    print('Error: number of given scans non consistent!')
    gate='skip';
    
if gate !='skip':
    RIXS_files_in_dir=[]; NORM_files_in_dir=[]; 
    buf1=[]; buf2=[]; 

    for r, d, f in os.walk(os.getcwd()):
        for indexf in range(0,len(RIXS_area)):
            for item in f:
                if str(RIXS_area[indexf]) in item:
                    RIXS_files_in_dir.append(item)

    for r, d, f in os.walk(os.getcwd()):
        for indexf in range(0,len(XES_norm)):
            for item in f:
                if str(XES_norm[indexf]) in item:
                    NORM_files_in_dir.append(item)
    
    d_norm=[]; 
    d_emono=[]; d_exes=[]; d_ffi0=[];
    for index in range(0,len(RIXS_files_in_dir)):
        buf2=np.loadtxt(NORM_files_in_dir[index]);
        d_norm=np.max(buf2[:,col_ffi0]);
                   
        buf1=np.loadtxt(RIXS_files_in_dir[index]);
        d_emono=np.append(d_emono, buf1[:,col_e_mono] );
        d_exes=np.append(d_exes, buf1[:,col_e_XES] );
        d_ffi0=np.append(d_ffi0, buf1[:,col_ffi0] /d_norm );
        
        
###############################################################################
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#plt.plot(d_emono, d_ffi0,'.')
ax.scatter(d_exes, d_emono, d_ffi0, cmap='coolwarm',c=d_ffi0)
ax.set_xlabel('Emission Energy (eV)')
ax.set_ylabel('Excitation Energy (eV)')
ax.set_zlabel('Normalised Intensity (Arb. Units)')
#plt.colorbar()
plt.draw()
plt.show()

###############################################################################
answer = input('Should I save your normalised data in a file (yes/no): ')
if answer.lower().startswith("y"):
    with open(OUT_NAME, 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        f.write("# Mono Energy \t XES Energy \t Norm. Intensity \n")
        writer.writerows( zip(d_emono, d_exes, d_ffi0) )
    print("Job done, live long and prosper!")
if answer.lower().startswith("n"):
    print('Job done, live long and prosper!')