import numpy as np
import matplotlib.pyplot as plt
import os

def read_osoaa(fname):
    with open(fname,'rb') as f:
        for ii in range(29):
            line = f.readline()    

        while line:
            vals = [float(x) for x in line.split()]
            line = f.readline()
            if vals[0]==0:
                refl=vals[3]
                refl_pol=vals[-1]
                break

    return refl,refl_pol


wl=np.arange(0.4,0.9001,0.005)


refl_toa=np.zeros(wl.size)+np.nan
refl_pol_toa=np.zeros(wl.size)+np.nan

refl_boa=np.zeros(wl.size)+np.nan
refl_pol_boa=np.zeros(wl.size)+np.nan

for i in range(wl.size):
    # TOA
    fname=os.environ['OSOAA_ROOT']+'/example_RESULTS/wl{:.3f}_level{}/Standard_outputs/RESLUM_vsVZA.txt'.format(wl[i],1)
    refl_toa[i],refl_pol_toa[i]=read_osoaa(fname)
    
    # BOA
    fname=os.environ['OSOAA_ROOT']+'/example_RESULTS/wl{:.3f}_level{}/Standard_outputs/RESLUM_vsVZA.txt'.format(wl[i],3)
    refl_boa[i],refl_pol_boa[i]=read_osoaa(fname)
    
plt.figure(figsize=(8,3))
plt.subplot(1,2,1)
plt.plot(wl*1000,refl_toa,'b',label='reflectance')
plt.plot(wl*1000,refl_pol_toa,'r',label='polarized reflectance')
plt.xlabel('Wavelength, nm')
plt.ylabel('TOA Reflectance')
plt.legend()
plt.subplot(1,2,2)
plt.plot(wl*1000,refl_boa,'b',label='reflectance')
plt.plot(wl*1000,refl_pol_boa,'r',label='polarizedreflectance')
plt.xlabel('Wavelength, nm')
plt.ylabel('BOA Reflectance')
plt.tight_layout()
plt.savefig('OSOAA_sim_refl.png')