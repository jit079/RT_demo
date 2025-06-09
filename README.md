<H1>Radiative Transfer Packages</H1>


<UL>
<LI> <b>Second Simulation of a Satellite Signal in the Solar Spectrum code (6S)</b>
  <UL>
  <LI> The <A HREF="https://salsa.umd.edu/6spage.html">official web site</A> has the latest software and documentation: 6SV2.1 (2014)
  <LI> Download <A HREF="6S/6sv4.1.zip" download>6s (1997) Code</A> (zip)
  <LI> User Guide, PDF: <A HREF="6S/6s_Manual_P1.pdf">part1</A>, <A HREF="6S/6s_Manual_P2.pdf">part2</A>, <A HREF="6S/6s_Manual_P3.pdf">part3</A></A>
  <LI> <A HREF="6S/6S_how_to.txt">How to run 6S</A> (txt)
  <LI> Examples of 6S inputs and outputs
  <UL>
  <LI>Example 1: <A HREF="6S/examples/example_input1.txt">input</A>, <A HREF="6S/examples/example_output1.txt">output</A> 
  <LI>Example 2: <A HREF="6S/examples/example_input2.txt">input</A>, <A HREF="6S/examples/example_output2.txt">output</A> 
  <LI>Example 3: <A HREF="6S/examples/example_input3.txt">input</A>, <A HREF="6S/examples/example_output3.txt">output</A> 
  <LI>Example 4: <A HREF="6S/examples/example_input4.txt">input</A>, <A HREF="6S/examples/example_output4.txt">output</A> 
  </UL>
  <LI><A HREF="6S/6S_example_description.txt">Example of typical simulations</A>: <A HREF="6S/6S_typical_sim.py">code</A>, <A HREF="6S/6S_typical_sim.png">output figures</A> 
  <LI>Something you may be interested in: <A HREF="https://py6s.readthedocs.io/en/latest/#">Py6S - A Python interface to 6S</A>
  </UL>

<LI><b>Atmospheric Radiative Transfer Database for Earth Climate Observation</b> (ARTDECO, <A HREF="https://www.icare.univ-lille.fr/artdeco/"> official web site</A>)
  <UL>
  <LI> <A HREF="ARTDECO/artdeco.zip">artdeco.zip</A>, <A HREF="https://drive.google.com/file/d/11BIyaYWRdAeI2Ba2mWwVHINoHup8lCpN/view?usp=share_link">data_artdeco.zip</A>, both need to be downloaded. 
  <LI> <A HREF="ARTDECO/ARTDECO_how_to.txt">How to run ARTDECO</A>
  <LI> <A HREF="ARTDECO/ARTDECO_example_description.txt">Example of typical simulations</A>: <A HREF="ARTDECO/example_use.py">code</A>, output figures (<A HREF="ARTDECO/flux.png">TOA and BOA flux</A>, <A HREF="ARTDECO/rad.png">TOA radiance</A>, <A HREF="ARTDECO/refl.png">TOA reflectance</A>)
  <LI> <A HREF="ARTDECO/notes.txt">Details regarding the example code</A>
  </UL>

<LI> <b>Ocean Successive Orders with Atmosphere - Advanced (OSOAA)</b>
  <UL>
  <LI> Code can be downloaded <A HREF="OSOAA/OSOAA_V2.0.zip" download>here</A> or through <A HREF="https://github.com/CNES/RadiativeTransferCode-OSOAA">GitHub</A>.
  <LI> <A HREF="OSOAA/OSOAA_V2.0/doc/OSOAA-V2.0_UserManual-V2.0.pdf">User Manual</A>
  <LI> <A HREF="OSOAA/OSOAA_V2.0/doc/OSOAA_TUTORIAL_V2.0.pdf">OSOAA Tutorial (how to install and run OSOAA with examples)</A>
  <LI> <A HREF="OSOAA/OSOAA_example_description.txt">Example of typical simulations</A>: <A HREF="OSOAA/run_OSOAA_example.ksh">code</A>, <A HREF="OSOAA/plot_OSOAA.py">python script to display results</A>, <A HREF="OSOAA/OSOAA_sim_refl.png">output figures</A>
  </UL>

<LI> <b>Speed-up Monte Carlo Advanced Radiative Transfer Code using GPU (SMART-G)</b>
  <UL>
  <LI> Both the code and installation guide are available at <A HREF="https://github.com/hygeos/smartg">HYGEOS GitHub site</A>. Follow the guide and you should have no problem installing SMART-G. However, be aware that it requires GPU for running the code.
  <LI> Example runs are also provided in the folder 'notebooks'.
  <LI> SMART-G runs in Python environment and requires conda, for which the installation guide can be found <A HREF="https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html">here</A>.
  <LI> <A HREF="SMARTG/SMARTG_example_description.txt">Example of typical simulations</A>: <A HREF="SMARTG/SMARTG_example.py">code</A>, <A HREF="SMARTG/par_5nm.zip">data needed for running the code</A>, <A HREF="SMARTG/SMARTG_example.png">output figures</A>
</UL>


