import os, sys
sys.path.insert(0, os.path.dirname(os.getcwd()))
from smartg.smartg import Smartg, Sensor
from smartg.smartg import RoughSurface, LambSurface, FlatSurface, Environment, Albedo_cst
from smartg.atmosphere import AtmAFGL, AerOPAC, Cloud
from smartg.water import IOP_1, IOP
from smartg.kdis import KDIS, reduce_kdis
import numpy as np
import matplotlib.pyplot as plt

# Spectrum
# read the entire K-distribution definition from files
kpar=KDIS('par_5nm','/media/jit079/nvme0n1/PAR/Kdistribution/par_5nm/')

bands    = kpar.to_smartg(lmin=300., lmax=900.)
NL = len(bands.l); 
_,w,solar_flux,_,_ ,_= bands.get_weights()


# WATERS
DEPTH  = 15. # bottom depth (m)
ALB    = 0.3 # albedo of the sea floor
chl    = 0.1 # (mg/m3) 
ws     = 5. # wind speed

# water model is from 400 to 700 nm. Values outside the range are assigned as those at 400 nm or 700 nm.
water = IOP_1( chl   = chl,
              DEPTH = DEPTH,
              pfwav = [550.],
              ALB   = Albedo_cst(ALB)
            ).calc(list(bands.get_weights()[1].data))
            
surf = RoughSurface(WIND=ws*1., NH2O=1.34)

# Atmosphere
wref   = 550. # reference wavelength (nm)
pfwav  = [550.] # wavelengths where aerosols phase function # is computed

# Static parameters
zsurf  = 0. # surface altitude (km)
vertical_grid    = [100., 50,  20., 10., 5., 1., zsurf] # vertical grid, from TOA to zsurf
atmosphere_model = 'afglus'  # AFGL US62 model

Psea   = 1012.15 # sea level atmospheric pressure
aer_model = 'maritime_clean'
aot = 0.1 # aerosol optical thickess at 550 nm
O3=300. # ozone amount, dobson
H2O=2. # water vapor, g/cm2
cot=5. # cloud optical thickess at 550 nm

# with an aerosol layer and a cloud layer
comps = [AerOPAC(aer_model, aot, wref),\
        Cloud('wc', 11., 2, 4, cot, wref)]
        
atm = AtmAFGL(atmosphere_model,   
               comp  = comps,
               O3    = O3,
               H2O   = H2O,  
               P0    = Psea, 
               grid  = vertical_grid,
               pfwav = pfwav
               ).calc(bands.l)

th0= 30.
VZA= 0.
RAA= 90.

# In order to compute accurately radiances in particular directions, set the LE mode
# 'le' keyword is a dictionnary containig directions vectors (in radians or deg) and coded as float32
# by default the result is calculated for each Ntheta x Nphi combination
le={'th_deg':VZA, 'phi_deg':RAA}

M = reduce_kdis(Smartg().run(THVDEG=th0, wl=bands.l, NBPHOTONS=1e9, 
                             water=water, BEER=1, le=le,
                             atm=atm, surf=surf, NF=10000, OUTPUT_LAYERS=3, flux=None,reflectance=True,
                             progress=False), bands, use_solar=False, integrated=False)  

print(M.describe())

plt.figure(figsize=(8,3))
plt.subplot(1,2,1)
plt.plot(M.axes['wavelength'],M['I_up (TOA)'][:,0,0],'b',label='reflectance')
plt.plot(M.axes['wavelength'],np.sqrt(M['Q_up (TOA)'][:,0,0]**2+M['U_up (TOA)'][:,0,0]**2+M['V_up (TOA)'][:,0,0]**2),'r',label='polarized reflectance')
plt.xlabel('Wavelength, nm')
plt.ylabel('TOA reflectance')
plt.legend()
plt.subplot(1,2,2)
plt.plot(M.axes['wavelength'],M['I_up (0+)'][:,0,0],'b')
plt.plot(M.axes['wavelength'],np.sqrt(M['Q_up (0+)'][:,0,0]**2+M['U_up (0+)'][:,0,0]**2+M['V_up (0+)'][:,0,0]**2),'r')
plt.xlabel('Wavelength, nm')
plt.ylabel('BOA reflectance')
plt.tight_layout()
plt.savefig('SMARTG_example.png')
