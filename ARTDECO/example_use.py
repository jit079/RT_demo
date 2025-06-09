#!/usr/bin/env python

# This was developped by Mathieu Compiegne at HYGEOS


# This code simulates BOA and TOA irradiance/reflectance for a typical atmosphere (Ozone 300 Dobson, pressure 1000 mb, and water vapor 2 g/cm^2) with maritime aerosols (AOT550=0.05,humidity 90.0%, scale height of 2 km) and a typical ocean surface (Chl=0.1 mg/m3, salinity 34.3 ppt, wind speed 5 m/s), with SZA, VZA, and RAZ of 20, 30, 90 degrees. 

from __future__ import print_function, division, absolute_import
from builtins import range

import os
import sys
import numpy as np
import pylab as plt
import time

########################################

dir_artdeco   = "/media/jit079/nvme0n1/ARTDECO/artdeco/fortran/"
dir_pyartdeco = "/media/jit079/nvme0n1/ARTDECO/artdeco/pyartdeco/"
dir_data      = "/media/jit079/nvme0n1/ARTDECO/data_artdeco/"
sys.path.append(dir_pyartdeco+'f2py_utils/')
import pyartdeco_runlib as pyartdeco
from f2py_utils import run_artdeco


########################################
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx



def launch_artdeco():

    # NOTE: wavelengths are all given in microns 

    ###########################################
    # artdeco_in technical parameters structure

    # wavel can be used to restrict the computation to wavelengths between 
    # these boundaries
    wavel     =[0.4,1.1]
    # number of computationnal streams
    nstreams_init = 8
    # nmat = 1: I is computed
    # nmat = 3: I, Q and U are computed
    nmat=1

    # you should probably not change the following keywords
    keywords  = ['nowarn', 'od_no_check']    
    kdis_model = "ckdmip_hypernav_mergedmixed"
    mode      = 'kdis ' + kdis_model
    filters  = ['none']
    trunc_method="dm"
    rt_model="doad"
    corint=True
    thermal=False

    artdeco_in = pyartdeco.artdeco_in(keywords, mode, filters, wavel,        \
                                        trunc_method, nstreams_init, rt_model, \
                                        corint, thermal, nmat)
        
    ####################
    # read kdis coeff
    print(" read kdis...")
    #   NOTE that the O2 actually includes  absorption for CH4, CO2, N2O
    #   for the kdistribution "ckdmip_hypernav_mergedmixed"
    #   The relative molar fraction between O2, CH4, CO2 and N2O is then fixed
    #                            XCO2 / XO2 = 1.977132e-03
    #                            XCH4 / XO2 = 8.953942e-06
    #                            XN2O / XO2 = 1.570779e-06
    kdis = pyartdeco.kdis_coeff(artdeco_in, dir_data+kdis_model+"/", 'h5')
    
    ######################
    # load solar TOA flux
    print(" read solar irradiance...")
    solrad = pyartdeco.solar_irradiance(artdeco_in, file_path=dir_data+kdis_model+"/kdis_"+kdis_model+".h5", file_format="h5_kdis")
    

    ###############################
    #   set ptcle structure
    opt_interp = True
    
    wlref      =  0.550       # refrerence wavelength to which the optical depth is given
    wlptcle    = [0.1, 100.0] # the reading of optical properties files will be restricted to that boundaries, this should be consistent with the computation you want to make, otherwise it will complain 

    # this is a list of particle that will enter atmosphere composition
    # Each particle is defined by a dictionnary
    # {"file_path": optical properties HDF5 file,               
    #  "name": name of the particle (must be consistent with names written in the HDF5 file (groups in file),
    #  "tau": optical depth (given at wvref as above)
    #  "humidity": (if aerosol) humidity between 0 and 100, depending on what is sampled in the optical properties file
    #  "alt_distrib": 
    #                   "sh"           for scale height (exponential decay), if so, "z" is required
    #                   "homogeneous"  homogeneous layer, if so, "z" (layer top altitude) and "dz": thickness of the layer is required
    #  "z": in km
    #  "dz": in km
    # "reff": effective  radius in micron; required for cloud (allowed range depends on what is sampled in  optical properties file)} 
    #             
    # Particles will be added with respect to that in layers as defined by the levels of atmophere (in atmospheric definition file)
    ptcle_def  = [  {"file_path":dir_data+"opt_opac.h5",               "name":"opac_maritime_clean", "tau":0.05, "humidity":90.0, "alt_distrib":"sh", "z":2.0 },
                    # {"file_path":dir_data+"opt_opac.h5",               "name":"opac_desert", "tau":0.1, "humidity":90.0, "alt_distrib":"sh", "z":8.0 },
                    # {"file_path":dir_data+"opt_libradtran_liquid.h5",  "name":"libradtran_liquid", "tau":12.0, "reff":14.0, "alt_distrib":"homogeneous", "z":2.0, "dz":2.0 } ,
                    # {"file_path":dir_data+"opt_baum_ice_ghm.h5",       "name":"ghm", "tau":0.2, "reff":60.0, "alt_distrib":"homogeneous", "z":10.0, "dz":1.0 }  
                    ]

    print(" read cloud/aer optical properties...")
    ptcle_opt  = pyartdeco.ptcle_optical_properties(ptcle_def, artdeco_in.nstreams, wlptcle,  wlref, opt_interp=opt_interp)
    print(" set cloud/aer structure...")
    ptcle      = pyartdeco.particle(artdeco_in, ptcle_def, ptcle_opt)    


    ########################
    # set surface structure
    name      = "ocean"
    family    = "brdf"
    kind      = "ocean"

    # Two options availables for the water leaving reflectance:
    # if use_morel is True
    #   the Morel, A., Optical modeling of the upper ocean in relation to its biogenous matter content (case I waters) 1988-09, jgr , Vol. 93, p. 10749-10768 
    #   case I water model is used, the pigment concentration (in mg/m^3) must be provided
    # if  use_morel is False
    #   Rsw (the irradiance reflectance) must be provided (together with the corresponding wavelength wvl_Rsw), it will be interpolated to relevant wavelengths if interp=True
    use_morel = True
    
    # in modelling the surface reflectance
    #    shadow           for shadowing effects (for glitter) to be accounted for or not 
    #    ocean_whitecaps  for whitecaps to be accounted for or not

    print(" set surface structure...")

    if use_morel:
        surface = pyartdeco.surface(name, family, kind, \
                    wdspd = 5.0, xsal=34.3, \
                    pcl = 0.1 , # pigment concentration (in mg/m^3)
                    shadow=True, ocean_whitecaps=True)
    else:
        wvl_Rsw  = np.array([0.1, 0.4, 0.5, 0.6, 0.7, 10.0])  # microns
        Rsw      = np.array([0., 0.01, 0.02, 0.02, 0.0, 0.0]) # irradiance reflectance
        surface = pyartdeco.surface(name, family, kind, \
                    wdspd = 5.0, xsal=34.3, \
                    wvl_Rsw=wvl_Rsw,  Rsw=Rsw, \
                    shadow=True, ocean_whitecaps=True, interp=True)


    ########################
    #      Geometry
    # sza = np.array([ 20.0, 30 ])
    # vza = np.array([ 30.0, 10.0, ])     
    # vaa = np.array([ 56.0, 58 ])

    sza = np.array([ 20.0 ])
    vza = np.array([ 30.0 ])     
    vaa = np.array([ 90.0])

    print(" set surface structure...")
    geom = pyartdeco.geometry(sza, vza, vaa)


    ####################
    #  load atmosphere
    # 

    atm  = 'atm_afgl_us62_red.dat' # atmospheric profiles (mostly contains z, P, T, air density, H2O density and O3 density)
    #                                the other gases quantities are definied regarding air density ("well mixed" gases) through gas_ppmv
  

    gas  = ["o2", "o3", "h2o"] # list of gas that will be accounted for for molecular absorption
    #                            NOTE that the O2 actually includes  absorption for CH4, CO2, N2O
    #                            for the kdistribution "ckdmip_hypernav_mergedmixed"
    #                            The relative molar fraction between O2, CH4, CO2 and N2O is then fixed
    #                            XCO2 / XO2 = 1.977132e-03
    #                            XCH4 / XO2 = 8.953942e-06
    #                            XN2O / XO2 = 1.570779e-06

    ppmv = [ 208493.3747, -1, -1]

    wldepol  = np.array([0.1, 200.0]) # microns
    depol    = np.array([0.0,   0.0]) # depolarisation factor 

    print(" read/set atmosphere structure...")
    atmos = pyartdeco.atmosphere(artdeco_in, dir_data, atm, gas, ppmv, 'ascii', wldepol, depol, interp=True, kdis=kdis, DU_o3=300,P0=1000,water=2)


    # Calling ARTDECO

    lamb, rad, rad_levels, flux, alt = run_artdeco(artdeco_in, atmos, surface, solrad, ptcle, geom, kdis=kdis, verbose=True)

    #    lamb       : wavelengths (microns)
    #    rad        : TOA (upwelling) radiances (W m-2 sr-1), dimensions (nsza,nvza,nvaa,nmat,nlambda) with nmat= 1 (I) or 3 (I,Q,U)
    #    rad_levels : radiances at each level of the atmosphere (W m-2 sr-1), dimensions (nsza,nvza,nvaa,nmat,nalt_atm,nlambda) with nmat= 1 (I) or 3 (I,Q,U),  levels correspond to atmospheric definition file
    #    flux       : flux (W m-2),  dimensions (nsza, 3, nalt_atm, nlambda), 3 values are downwelling / upwelling / directional downwelling
    #    alt        : levels in km  (corresponding to atmospheric definition file)

    plt.figure()
    plt.plot(lamb*1000, rad[0,0,0,0,:]/0.5) # simulated rad is in W m-2 sr-1, divided by 0.5 nm (the resolution of the simulation)
    plt.xlabel('Wavelength, nm')
    plt.ylabel('TOA radiance, W/m2/nm/sr')
    plt.savefig("rad.png")
    
    plt.figure()
    plt.plot(lamb*1000,  flux[0,0,0,:]/0.5, label="downwelling flux TOA")
    plt.plot(lamb*1000,  flux[0,2,-1,:]/0.5, label="direct downwelling flux BOA")
    plt.plot(lamb*1000,  (flux[0,0,-1,:]-flux[0,2,-1,:])/0.5, label="diffuse downwelling flux BOA")
    plt.legend(loc="best")
    plt.xlabel('Wavelength, nm')
    plt.ylabel('Irradiance, W/m2/nm')
    plt.savefig("flux.png")

    plt.figure()
    plt.plot(lamb*1000, np.pi * rad[0,0,0,0,:] / flux[0,0,0,:])
    plt.xlabel('Wavelength, nm')
    plt.ylabel('TOA reflectance')
    plt.savefig("refl.png")

    return






    
if __name__=='__main__':
   

    launch_artdeco()




