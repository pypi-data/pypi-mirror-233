# GWToolbox
The pdf version of the user manul (installation and usage of the python package) can be found here:
https://gw-universe.org:4432/Documents/user_manual.pdf

# Installation:
The package is composed of three modules, namely the ground-based detectors (and their targets), the space-borne detectors (and their targets) and pulsar timing arrays (PTA). These three modules work independently, and have
different dependencies on other packages and libraries. That means failed dependencies met in one module will not influence the usage of another module.
The three modules depend on some common python packages: numpy, scipy, multiprocessing, pandas, astropy.

I will introduce the dependencies indiviudally for the three modules in the following subsections. After the dependencies installed, the GWToolbox package can be directly imported, after you set the environment variable:

export PYTHONPATH=folder_contain_gwtoolbox/gwtoolbox

or, cd to folder_contain_gwtoolbox/gwtoolbox, and run

python setup.py install

this will install the python packages into your default path for python packages.

1. Ground-based detectors module
The functionality of simulating the noise properties of customised LIGO-like detec- tors is realized with PyKat1. It is a python wrapper for of the detector simulation tool FINESSE2. Make sure the environment variables FINESSE_DIR and KATINI are set correctly towards the folder containing executable kat.

The fast way to install FINESSE and PyKat is to run the command line:
conda install -c gwoptics pykat

2. Space-borne detectors
This module depends on the codes inside the Mock LISA data challenge (MLDC). The relevant parts of MLDC is already included in the GWToolbox:
/gwtoolbox/gwtoolbox/MLDC-master,
cd to the directory /MLDC-master/Packages and run: 

python setup_lisaxml2.py install

then cd to the directory /MLDC-master/Packages/common and run:

python setup.py install

to install common packages needed by MLDC. Then to install packages that simulate the waveform of sources respectively: cd to the directory /MLDC-master/Waveforms/MBH_IMR/IMRPhenomD and run:

make 

to install tools to simulate waveforms of supermassive black hole binary mergers. cd to the directory /MLDC-master/Waveforms/fastGB and run:

python setup.py install

to install tools to simulate waveforms of Galactic compact binaries.
The simulation on the waveform of EMRIs depends on an other tool EMRI_Kludge_Suite3.
In the original EMRI_Kludge_Suite, the arm-length of LISA is hard-coded. I revised the source code to enable a different arm-length. The revised EMRI_Kludge_Suite is included in the GWToolbox: /gwtoolbox/gwtoolbox/EMRI_Kludge_Suite, cd to this directory, and run:

make 

to build the binaries. The GSL and FFTW libraries are required for compilation. After this step, you will need to install the python wrapper. Make sure that in the setup.py, the variables gsl and gslcblas are set correctly to the path of the libraries, and make sure that your environment variable LD_LIBRARY_PATH is set properly so that the required libraries can be found. Then run:

python setup.py install

3. Pulsar Timing Arrays
This module has no special dependencies.

Happy gravitational-wave-simulating!

Additional info:
# Authors:
Shu-Xu Yi, Zuzanna Kostrzewa-Rutkowska, Christiaan Brinkerink
# Contact:
S.Yi@astro.ru.nl
# How to cite
check the cite info in https://gw-universe.org:4432/about.html
# Licence:
GNU GPL v3

