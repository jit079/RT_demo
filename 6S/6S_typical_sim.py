#This code simulate TOA reflectance and downwelling irradiance, for typical atmosphere, typical ocean, and geometry, as a function of wavelength, from 350 to 900 nm by step of 5 nm.

import numpy as np
import os
import matplotlib.pyplot as plt

def write_6S_input(filename,solzen,solaz,vzen,vaz,month,day,watvap,o3,aot550,ws,winf,wsup):
    f=open(filename,'w')
    f.write('0 (User defined)\n')
    f.write('%f %f %f %f %d %d\n' % (solzen,solaz,vzen,vaz,month,day))
    f.write('8\n')
    f.write('%f %f\n' % (watvap,o3))
    f.write('2 Maritime Model\n')
    f.write('0\n')
    f.write('%f value\n' % aot550)
    f.write('0 (target level)\n')
    f.write('-1000 (sensor level)\n')
    f.write('0\n')
    f.write('%f %f\n' % (winf/1000,wsup/1000))
    f.write('0 Homogeneous surface\n')
    f.write('1 (dirctional effects)\n')
    f.write('6 Ocean\n')
    f.write('%f 45 35 %f\n' % (ws,chl))
    f.write('-2 No atm. corrections selected\n')
    f.close()

def read_6S_output(filename):
    f=open(filename,'r')
    lines=f.readlines()
    f.close()
    for i in range(len(lines)):
        line=lines[i]
        if "apparent reflectance" in line:
            rho_toa=float(line.split()[3])
            rad_toa=float(line.split()[6])
        if "irr. at ground level (w/m2/mic)" in line:
            line3=lines[i+2]
            irad_boa=float(line3.split()[1])+float(line3.split()[2])+float(line3.split()[3])
    return rho_toa,rad_toa,irad_boa


if not os.path.exists('input'):
    os.system('mkdir input') # create a folder 'input' to save all the 6S input files

if not os.path.exists('output'):
    os.system('mkdir output') # create a folder 'output' to save all the 6S output files

month=1
day=1
sza=30. # solar zenith
vza=45. # view zenith
saz=0. # solar azimuth
vaz=90. # view azimuth
watvap=2.  # water vapor, g/cm2
o3=0.3 # ozone, cm-atm
aot550=0.1 # aerosol optical thickness @ 550 nm
ws=5 # wind speed, m/s
chl=0.1 # chlorophyll concentration, mg/m3
wl=np.arange(400,901,5) # from 400 to 900 nm by step of 5 nm

rho_toa=np.zeros(wl.size)+np.nan
rad_toa=np.zeros(wl.size)+np.nan
irad_boa=np.zeros(wl.size)+np.nan

for i in range(wl.size):
    write_6S_input('input/sim_{}.txt'.format(wl[i]),\
                   sza,saz,vza,vaz,month,day,watvap,o3,aot550,ws,wl[i]-2.5,wl[i]+2.5)
    
    os.system('6sv4.1/sixs < input/sim_{}.txt > output/sim_{}.txt'.format(wl[i],wl[i]))
    
    rho_toa[i],rad_toa[i],irad_boa[i]=read_6S_output('output/sim_{}.txt'.format(wl[i]))


        
plt.figure(figsize=(12,3))
plt.subplot(1,3,1)
plt.plot(wl,rho_toa)
plt.xlabel('Wavelength, nm')
plt.ylabel('TOA reflectance')
plt.subplot(1,3,2)
plt.plot(wl,rad_toa)
plt.xlabel('Wavelength, nm')
plt.ylabel('TOA radiance, W/m2/sr/mic')
plt.subplot(1,3,3)
plt.plot(wl,irad_boa)
plt.xlabel('Wavelength, nm')
plt.ylabel('BOA irradiance, W/m2/mic')
plt.tight_layout()
plt.savefig('6S_typical_sim.png')
plt.close()
