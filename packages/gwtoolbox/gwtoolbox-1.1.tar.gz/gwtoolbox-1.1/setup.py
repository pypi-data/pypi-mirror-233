from setuptools import setup
from setuptools.command.install import install
import subprocess

class CustomInstallCommand(install):
	def run(self):
		subprocess.run(['sh', 'install_dependencies.sh'])
		install.run(self)


dependencies = ['numpy','scipy','astropy','matplotlib','pykat','pycbc']
# above are the denpendencies available in pip
 

#dependencies = ['numpy','scipy','astropy','matplotlib','pykat','common','pyIMRPhenomD','FastBinary','AAKwrapper','pycbc']

#dependencies = ['numpy','scipy','astropy','matplotlib','pykat']
setup(name='gwtoolbox',
      version='1.1',
      description='Gravitational Wave Tools',
      url='https://gw-universe.org/',
      packages=['gwtoolbox'],
      package_data={'gwtoolbox': ['data_detectors/*.txt','*.rst','*.dat','*.txt','accessory/*.txt','accessory/*.dat','catalogues_mHz/*']},
      scripts=[],
      install_requires=dependencies,
      cmdclass={
	'install':CustomInstallCommand,
	},      
)
