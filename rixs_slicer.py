# -*- coding: utf-8 -*-
"""
Script to slice and integrate RIXS data along user-selected line
"""
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

buf=np.loadtxt('Normalised_RIXS.dat');
d_emono=buf[:,0]; d_exes=buf[:,1]; d_ffi0=buf[:,2];        
        
a=np.where(d_emono>np.max(d_emono)-0.01)
period=a[0][0]
xas=np.ones(period)
e_transfer=d_emono-d_exes
for index in range(0,period):
    xas[index]=sum(d_ffi0[index::period+1])

###############################################################################
fig = plt.figure()
gs = gridspec.GridSpec(2, 2)

ax1 = fig.add_subplot(gs[:,0], projection='3d')
#plt.plot(d_emono, d_ffi0,'.')
ax1.scatter(d_emono, d_exes, d_ffi0, cmap='coolwarm',c=d_ffi0)
ax1.set_xlabel('Incident Energy (eV)')
ax1.set_ylabel('Excitation Energy (eV)')
ax1.set_zlabel('Normalised Intensity (Arb. Units)')

ax2 = fig.add_subplot(gs[0, 1])
ax2.scatter(d_emono, e_transfer, 500*d_ffi0, cmap='coolwarm',c=d_ffi0)
ax2.set_xlabel('Incident Energy (eV)')
ax2.set_ylabel('Energy Transfer (eV)')
plt.title('Intensity *500')

ax3 = fig.add_subplot(gs[1, 1])
ax3.plot(d_emono[0:period], xas)
ax3.set_xlabel('Incident Energy (eV)')
ax3.set_ylabel('Integrated Intensity (Arb. U.)')
plt.title('Slice along the energy transfer')
plt.draw()
plt.show()

###############################################################################
# Here below slicing manual slicing-option for RIXS in energy-trnsfer plot

print('Click on the extremes of your slice, then press return!')

window=1 # window of 1eV around User-defined line
bufsel =plt.ginput(-1)
bufsel=np.asarray(bufsel); Xsel=bufsel[:,0]; Ysel=bufsel[:,1]

b=np.where( (d_emono>np.min(Xsel)-window) & (d_emono<np.max(Xsel)+window) )
period2=[];
for index in range(1,len(b[0])):
    if b[0][index]-b[0][index-1] > 1:
        period2=np.append(period2,index);

if 'rixs_int' in locals():
    del rixs_int
                
Tol=0.2; # Energy tolerance within data points in energy transfer       
buf_et=e_transfer[b[0]]; buf_int=d_ffi0[b[0]] 
rixs_e_grid=np.arange(min(Ysel),max(Ysel),Tol)
rixs_int=np.zeros((len(rixs_e_grid),1))

for index1 in range(0,len(buf_et)):
    for index2 in range(0,len(rixs_e_grid)): 
        if np.abs(buf_et[index1]-rixs_e_grid[index2])<Tol:
            rixs_int[index2]=rixs_int[index2]+buf_int[index1]
 

fig = plt.figure()
plt.subplot(1,2,1)
plt.plot(e_transfer[b[0]],d_ffi0[b[0]],'.')
ax3.set_xlabel('Energy Transfer (eV)')
ax3.set_ylabel('Intensity (Arb. U.)')
plt.title('Raw data in Energy-transfer window')

plt.subplot(1,2,2)
plt.plot(rixs_e_grid,rixs_int,'.')
ax3.set_xlabel('Energy Transfer (eV)')
ax3.set_ylabel('Intensity (Arb. U.)')
plt.title('Slice')
plt.draw()
plt.show()

###############################################################################
# I/O
answer = 'no' # input('Should I save your sliced data in a file (yes/no): ')
OUT_NAME='Slice_Mono%.2f_XESfrom%.2fto%.2f.dat' % (np.mean(Xsel), min(Ysel), max(Ysel) )

if answer.lower().startswith("y"):
    with open(OUT_NAME, 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        f.write("# Energy Transfer \t Integrated Intensity \n")
        writer.writerows( zip(rixs_e_grid, rixs_int) )
    print("Job done, live long and prosper!")
if answer.lower().startswith("n"):
    print('Job done, live long and prosper!')

