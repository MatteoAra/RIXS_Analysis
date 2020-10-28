# -*- coding: utf-8 -*-
"""
RIXS data plotter
"""

import numpy as np 
import matplotlib.pyplot as plt
import scipy as sp
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

############################################################### Data here below 
dbuf= np.loadtxt('Test_GDA9.14_122373_1.dat')
###############################################################

fig = plt.figure()
#ax = fig.gca(projection='3d')

#surf = ax.plot_surface(dbuf[:,1], dbuf[:,2], dbuf[:,5], cmap=cm.coolwarm, linewidth=0, antialiased=False)
#ax.plot_trisurf(dbuf[:,1], dbuf[:,2], dbuf[:,5], 'o', linewidth=0.2, antialiased=True)

plt.scatter(dbuf[:,1], dbuf[:,0], c=dbuf[:,4], cmap='Blues')
plt.xlabel('Emission Energy (eV)')
plt.ylabel('Excitation Energy (eV)')
plt.colorbar()
plt.show()

plt.show()
