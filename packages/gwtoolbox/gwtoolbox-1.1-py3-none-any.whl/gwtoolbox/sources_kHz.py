import numpy as np
from scipy.stats import truncnorm
from astropy import units as u
from multiprocessing import Pool
import time
from gwtoolbox.cosmology import Cosmology
from gwtoolbox.constants import *
from gwtoolbox.parameters import *
from gwtoolbox.functions_earth import *
import os.path
#import time
my_path = os.path.abspath(os.path.dirname(__file__))
path_angle = os.path.join(my_path, "accessory/angles.dat")
path_IS_et=os.path.join(my_path,"accessory/for_integral_et_BBH.txt")
path_IS_ligo=os.path.join(my_path, "accessory/for_integral_ligo_BBH.txt")
path_IS_med=os.path.join(my_path, "accessory/for_integral_med_BBH.txt")

path_IS_et_DNS=os.path.join(my_path, "accessory/for_integral_et_DNS.txt")
path_IS_ligo_DNS=os.path.join(my_path, "accessory/for_integral_ligo_DNS.txt")
path_IS_med_DNS=os.path.join(my_path, "accessory/for_integral_med_DNS.txt")

path_IS_ligo_BHNS=os.path.join(my_path, "accessory/for_integral_ligo_BHNS.txt")
path_IS_et_BHNS=os.path.join(my_path, "accessory/for_integral_et_BHNS.txt")
path_IS_med_BHNS=os.path.join(my_path, "accessory/for_integral_med_BHNS.txt")

path_IS_ligo_BGDNS=os.path.join(my_path, "accessory/for_integral_ligo_BGDNS.txt")


random_angles=np.loadtxt(path_angle)
theta_array = random_angles[:,0]
varphi_array = random_angles[:,1]
iota_array = random_angles[:,2]
psi_array = random_angles[:,3]


# an isotropic distribution of angles
para_IS_et=np.loadtxt(path_IS_et)
z_array_et = para_IS_et[:,0]
m1_array_et = para_IS_et[:,1]
m2_array_et = para_IS_et[:,2]

para_IS_et_DNS=np.loadtxt(path_IS_et_DNS)
z_array_et_DNS=para_IS_et_DNS[:,0]
m1_array_et_DNS=para_IS_et_DNS[:,1]
m2_array_et_DNS=para_IS_et_DNS[:,2]

para_IS_et_BHNS=np.loadtxt(path_IS_et_BHNS)
z_array_et_BHNS=para_IS_et_BHNS[:,0]
m1_array_et_BHNS=para_IS_et_BHNS[:,1]
m2_array_et_BHNS=para_IS_et_BHNS[:,2]



para_IS_ligo=np.loadtxt(path_IS_ligo)
z_array_ligo=para_IS_ligo[:,0]
m1_array_ligo=para_IS_ligo[:,1]
m2_array_ligo=para_IS_ligo[:,2]

para_IS_ligo_DNS=np.loadtxt(path_IS_ligo_DNS)
z_array_ligo_DNS=para_IS_ligo_DNS[:,0]
m1_array_ligo_DNS=para_IS_ligo_DNS[:,1]
m2_array_ligo_DNS=para_IS_ligo_DNS[:,2]

para_IS_ligo_BHNS=np.loadtxt(path_IS_ligo_BHNS)
z_array_ligo_BHNS=para_IS_ligo_BHNS[:,0]
m1_array_ligo_BHNS=para_IS_ligo_BHNS[:,1]
m2_array_ligo_BHNS=para_IS_ligo_BHNS[:,2]
#        z_array = np.random.lognormal(0.69,1.2,size=length)
#        m1_array = np.random.lognormal(2.7,0.5,size=length)
#        m2_array = np.random.lognormal(2.7,0.5,size=length)
# a distribution of parameter space which mimic the shape of the detected parameter density.
#
para_IS_med=np.loadtxt(path_IS_med)
z_array_med=para_IS_med[:,0]
m1_array_med=para_IS_med[:,1]
m2_array_med=para_IS_med[:,2]

para_IS_med_DNS=np.loadtxt(path_IS_med_DNS)
z_array_med_DNS=para_IS_med_DNS[:,0]
m1_array_med_DNS=para_IS_med_DNS[:,1]
m2_array_med_DNS=para_IS_med_DNS[:,2]

para_IS_med_BHNS=np.loadtxt(path_IS_med_BHNS)
z_array_med_BHNS=para_IS_med_BHNS[:,0]
m1_array_med_BHNS=para_IS_med_BHNS[:,1]
m2_array_med_BHNS=para_IS_med_BHNS[:,2]

class BHB:
    """
    This is a class to describe stellar mass black hole black hole mergers.

    Parameters:
      cosmos: define cosmological model

    """
    def __init__(self, cosmos):
        """
        Parameters:
          cosmos (class): define cosmological model
        """
        self.cosmos = cosmos
        #self.theta = thetaBHB
        #self.zs= np.logspace(-4, 1., 30)
        self.zs=np.linspace(1e-2,10,100)
        #self.Rm= np.zeros(len(self.zs))
        #self.chi_sigma=0.1
        self.pop='I'
    def set_model_theta(self, pop, new_theta=None):
        """
        The function to change theta from fiducial to user-defined in cosmic merger rate

        Parameters:
          new_theta (Optional[list of floats]): new parameter values

        Returns:
          (list of floats): theta with new values, if new_theta=None return theta to fiducial
        """
        self.pop=pop
        if pop=='I': # power law mass function with a hard cut
            if new_theta==None:
                self.theta=BBH_Pop1
            else:
                self.theta=new_theta
        #if np.array(new_theta).any() != None:
        #   self.theta = new_theta
            R0, tau, self.mu, self.c, self.gamma, self.mcut, self.q_low, self.chi_sigma = self.theta
            if not R0>0:
                raise ValueError("R0 must be positive")
            if not 100>tau>0.1:
                raise ValueError("We limit the range of tau from 0.1 to 100")
            if not self.mu>0:
                raise ValueError("mu needs to be positive")
            if not self.c>0:
                raise ValueError("c should be positive")
            if not self.gamma>1:
                raise ValueError("gamma should >1, otherwise can't normalise.")
            if not self.mcut>self.c/self.gamma+self.mu:
                raise ValueError("mcut should be larger than c/gamma+mu")
            if not 1>self.q_low>0:
                raise ValueError("q_low should be in between 0 and 1")
            if not self.chi_sigma>0:
                raise ValueError("chi_sig should be larger than 0")
            self.Rm=R0*R(self.zs, 2.7, 5.6, 2.9, tau, self.cosmos)
        elif pop=='II': # mass function: power law+peak
            if new_theta==None:
                self.theta = BBH_Pop2
            else:
                self.theta=new_theta
            R0, tau, self.mu, self.c, self.gamma, self.mcut, self.mpeak, self.mpeak_scale, self.mpeak_sig, self.q_low, self.chi_sigma = self.theta
            if not R0>0:
                raise ValueError("R0 must be positive")
            if not 100>tau>0.1:
                raise ValueError("We limit the range of tau from 0.1 to 100")
            if not self.mu>0:
                raise ValueError("mu needs to be positive")
            if not self.c>0:
                raise ValueError("c should be positive")
            if not self.gamma>1:
                raise ValueError("gamma should >1, otherwise can't normalise.")
            if not self.mcut>self.c/self.gamma+self.mu:
                raise ValueError("mcut should be larger than c/gamma+mu")
            if not self.mpeak>0:
                raise ValueError("mpeak should be larger than zero")
            if not self.mpeak_sig>0:
                raise ValueError("mpeak_sig should be larger than 0")
            if not 1>self.q_low>0:
                raise ValueError("q_low should be in between 0 and 1")
            if not self.chi_sigma>0:
                raise ValueError("chi_sig should be larger than 0")
            self.Rm=R0*R(self.zs, 2.7, 5.6, 2.9, tau, self.cosmos)
        elif pop=='III': # z-dependent mass function
            if new_theta==None:
                self.theta = BBH_Pop3
            else:
                self.theta=new_theta
            R0, tau, alpha, beta, C, self.mu0, self.mu1, self.c0, self.c1, self.gamma0, self.gamma1 , self.mcut, self.q0, self.q1, self.chi_sigma=self.theta
            self.Rm=R0*R(self.zs, alpha, beta, C, tau, self.cosmos)

        #else:
        #    self.chi_sigma=0.1
#           print (R(0.1, 2.7, 5.6, 2.9, tau, self.cosmos))
#           print ('shape of Rm is: %d; while the shape of zs is: %d' % (len(self.Rm),len(self.zs)))
    def mod_norm(self, Mch, F, iota, z):
        """
        The normalization constant of the modulus of the GW waveform from stellar-mass binary black holes (BHB) mergers in frequency domain.

        Parameters:
          Mch (1-D ArrayLike floats):  Red-shifted chirp mass of the BHB in solar masses
          F (array of dtype float): The Antenna Patterns of the observatory
          iota (Array of floatsfloat): The inclination of the BHB orbit
          z (float): The redshift of the GW source

        Returns:
          (float): The normalization of the GW strain
        """
        C = CONST_AMPLITUDE_GW*Mch**(5./6.)/self.cosmos.luminosity_distance(z).to_value(u.Gpc)
        scaling_factor = np.sqrt(((1.+np.cos(iota)**2)/2.)**2*F[0]**2+np.cos(iota)**2*F[1]**2)
        if np.isscalar(Mch)==True:
            return C*scaling_factor
        else:
            return np.einsum('i,j->ij',C,scaling_factor)

    def mod_shape(self, f):
        """
        The frequency dependence of the modulus of the GW waveform of BHB mergers.

        Parameters:
          f (float or array of dtype float): Frequencies of GW

        Returns:
          (float or array of dtype float): The modulus of the waveform corresponds to each frequency in f
        """
        return f**(-7./6.)
    def mod_shape_merger(self, f):
        # the shape of waveform in merger stage, it should be glue to the inspiral waveform.
        return f**(-2./3.)
    def mod_shape_ringdown(self, f, f2, sigma):
        if np.isscalar(f2):
            return 1./np.pi*0.5*sigma/((f-f2)**2+(0.5*sigma)**2)
        else:
        # the return should be dim(f2)*dim(f) dimensional matrix #29 Oct. 2021, by yishuxu
    	    return 1./np.pi*0.5*np.einsum('i,j->ij',sigma,np.ones(len(f)))/((np.einsum('i,j->ij',np.ones(len(f2)),f)-np.einsum('i,j->ij',f2,np.ones(len(f))))**2+(0.5*np.einsum('i,j->ij',sigma,np.ones(len(f))))**2)

    def etachi(self, eta, chi):
        """
        accept 1-D arrayLike eta and chi, but they must be the same length
        return an array of 3*3 np.array, the outer length is len(eta)
        """
        A=np.array([eta**0,eta, eta**2])
        B=np.array([eta**0,chi, chi**2])
        return np.einsum('i...,j...->...ij', B,A)
        #return np.array([[eta**i*chi**j for i in range(0,3)] for j in range(0,3)])

    def freq_limit_old(self, m1, m2, chi):
        """
        accept 1-D arrayLike m1,m2,chi, they shoule be in the same length.
        """
        M=m1+m2
        eta=sym_ratio(m1,m2) # this can be 1-D arrayLike, with same dimension with m1,m2
        y=np.zeros((3,3))
        y[(0,0)] = 0.6437
        y[(0,1)] = 0.827
        y[(0,2)] = -0.2706
        y[(1,0)] = -0.05822
        y[(1,1)] = -3.935
        y[(2,0)] = -7.092
        sum_freq = 1.-4.455*(1-chi)**0.217+3.521**(1-chi)**0.26
        a=self.etachi(eta, chi)
        result=sum_freq+np.einsum('ij,...ji',y,a)
        return result*c**3/(GM_sun*M*np.pi) #[Hz]

    def freq_limit(self, m1, m2, chi):
        """
        The frequency upper limit of the waveform (in insprial phase: shuxu, 29th Sep. 2021).

        Parameters:
          m1 (float): The Red-shifted individual masses
          m2 (float): The Red-shifted individual masses

        Returns:
          (float): The upper limit of the frequency
        """
        M = m1+m2
        eta = sym_ratio(m1,m2)
        y = np.zeros((4,3))
        y[(1,0)] = 0.6437
        y[(1,1)] = 0.827
        y[(1,2)] = -0.2706
        y[(2,0)] = -0.05822
        y[(2,1)] = -3.935
        y[(3,0)] = -7.092

        sum_freq = 1.-4.455*(1-chi)**0.217+3.521**(1-chi)**0.26
        for i in range(1,4):
            N = min(3-i,2)
            for j in range(0,N+1):  ### N -> N+1
                sum_freq += y[(i,j)]*eta**i*chi**j
        return c**3/(GM_sun*M*np.pi)*sum_freq # unit [Hz]

    def freq_limit_merger(self, m1, m2, chi):
        """
        The frequency upper limit of the waveform in merger stage, added by shuxu, 29th Sep. 2021

        Parameters:
          m1 (float): The Red-shifted individual masses
          m2 (float): The Red-shifted individual masses

        Returns:
          (float): The upper limit of the frequency
        """
        M = m1+m2
        eta = sym_ratio(m1,m2)
        y = np.zeros((4,3))
        y[(1,0)] = 0.1469
        y[(1,1)] = -0.1228
        y[(1,2)] = -0.02609
        y[(2,0)] = -0.0249
        y[(2,1)] = 0.1701
        y[(3,0)] = 2.325

        sum_freq = 0.5*(1-0.63*(1-chi)**0.3)
        for i in range(1,4):
            N = min(3-i,2)
            for j in range(0,N+1):  ### N -> N+1
                sum_freq += y[(i,j)]*eta**i*chi**j
        return c**3/(GM_sun*M*np.pi)*sum_freq # unit [Hz]
    def freq_limit_ringdown(self, m1, m2, chi):
        """
        The frequency upper limit of the waveform in ringdown stage, added by shuxu, 29th Sep. 2021

        Parameters:
          m1 (float): The Red-shifted individual masses
          m2 (float): The Red-shifted individual masses

        Returns:
          (float): The upper limit of the frequency
        """
        M = m1+m2
        eta = sym_ratio(m1,m2)
        y = np.zeros((4,3))
        y[(1,0)] = -0.1331
        y[(1,1)] = -0.08172
        y[(1,2)] = 0.1451
        y[(2,0)] = -0.2714
        y[(2,1)] = 0.1279
        y[(3,0)] = 4.922

        sum_freq = 0.3236+0.04894*chi+0.01346*chi**2
        for i in range(1,4):
            N = min(3-i,2)
            for j in range(0,N+1):  ### N -> N+1
                sum_freq += y[(i,j)]*eta**i*chi**j
        return c**3/(GM_sun*M*np.pi)*sum_freq # unit [Hz]
    def freq_sigma(self, m1, m2, chi):
        """
        The frequency span of the waveform in ringdown stage, added by shuxu, 29th Sep. 2021

        Parameters:
          m1 (float): The Red-shifted individual masses
          m2 (float): The Red-shifted individual masses

        Returns:
          (float): The upper limit of the frequency
        """
        M = m1+m2
        eta = sym_ratio(m1,m2)
        y = np.zeros((4,3))
        y[(1,0)] = -0.4098
        y[(1,1)] = -0.03523
        y[(1,2)] = 0.1008
        y[(2,0)] = 1.829
        y[(2,1)] = -0.02017
        y[(3,0)] = -2.87

        sum_freq = (1-0.63*(1-chi)**0.3)*(1-chi)**0.45/4.
        for i in range(1,4):
            N = min(3-i,2)
            for j in range(0,N+1):  ### N -> N+1
                sum_freq += y[(i,j)]*eta**i*chi**j
        return c**3/(GM_sun*M*np.pi)*sum_freq # unit [Hz]
    def phase(self,f, m1, m2, chi, t0, phi0):
    #
    #        The phase of the waveform of the stellar-mass BHB mergers in the frequency domain.
    #
    #        Parameters:
    #          f (float or array of dtype float): Frequencies of GW
    #          m1 (float): Red-shifted mass of the prime BH
    #          m2 (float): Red-shifted mass of the second BH
    #          chi (float): spin
    #          t0 (float): The time of coalescence
    #          phi0 (float): The phase of coalescence
    #
    #        Returns:
    #          (array of dtype float): The phase psi(f) of the waveform as in exp{−ipsi(f)}
    #
        M = m1+m2
        eta = sym_ratio(m1,m2)
        x = np.zeros((3,3,6))
        x[(0,0,0)] = -920.9
        x[(0,1,0)] = 492.1
        x[(0,2,0)] = 135.0
        x[(1,0,0)] = 6742.
        x[(1,1,0)] = -1053.
        x[(2,0,0)] = -1.34e4
        x[(0,0,1)] = 1.702e4
        x[(0,1,1)] = -9566.
        x[(0,2,1)] = 2182.
        x[(1,0,1)] = -1.214e5
        x[(1,1,1)] = 2.075e4
        x[(2,0,1)] = 2.386e5
        x[(0,0,2)] = -1.254e5
        x[(0,1,2)] = 7.507e4
        x[(0,2,2)] = 1.338e4
        x[(1,0,2)] = 8.735e5
        x[(1,1,2)] = -1.657e5
        x[(2,0,2)] = -1.694e6
        #    x[(1,0,5)]=-920.9;x[(1,1,5)]=492.1;x[(1,2,5)]=135.0;x[(2,0,5)]=6742.;x[(2,1,5)]=-1053.;x[(3,0,5)]=-1.34e4
        x[(0,0,4)] = -8.898e5
        x[(0,1,4)] = 6.31e5
        x[(0,2,4)] = 5.068e4
        x[(1,0,4)] = 5.981e6
        x[(1,1,4)] = -1.415e6
        x[(2,0,4)] = -1.128e7
        x[(0,0,5)] = 8.696e5
        x[(0,1,5)] = -6.71e5
        x[(0,2,5)] = -3.008e4
        x[(1,0,5)] = -5.838e6
        x[(1,1,5)] = 1.514e6
        x[(2,0,5)] = 1.089e7
        Psi = lambda chi : np.array([3715./756.,-16.*np.pi+113.*chi*(1./3.),15293365.0/508032.0-405.*chi**2/8.0,0,0,0])
        #result = 1.
        v = (np.pi*M*f*GM_sun/c**3)**(1./3.) # dimensional less, total mass
        a=self.etachi(eta,chi)
        Temp=np.einsum('ijk,ji',x,a)+Psi(chi)
        b=np.array([v**(k+2) for k in range(0,6)])
        result=1.+np.einsum('i,i...',Temp,b)
        return 2.*np.pi*f*t0+phi0+3./128./eta/v**5*result

    def phase_old(self, f, m1, m2, chi, t0, phi0):
#
#        The phase of the waveform of the stellar-mass BHB mergers in the frequency domain.
#
#        Parameters:
#          f (float or array of dtype float): Frequencies of GW
#          m1 (float): Red-shifted mass of the prime BH
#          m2 (float): Red-shifted mass of the second BH
#          chi (float): spin
#          t0 (float): The time of coalescence
#          phi0 (float): The phase of coalescence
#
#        Returns:
#          (array of dtype float): The phase psi(f) of the waveform as in exp{−ipsi(f)}
#
        M = m1+m2
        eta = sym_ratio(m1,m2)
        x = np.zeros((4,3,8))
        x[(1,0,2)] = -920.9
        x[(1,1,2)] = 492.1
        x[(1,2,2)] = 135.0
        x[(2,0,2)] = 6742.
        x[(2,1,2)] = -1053.
        x[(3,0,2)] = -1.34e4
        x[(1,0,3)] = 1.702e4
        x[(1,1,3)] = -9566.
        x[(1,2,3)] = 2182.
        x[(2,0,3)] = -1.214e5
        x[(2,1,3)] = 2.075e4
        x[(3,0,3)] = 2.386e5
        x[(1,0,4)] = -1.254e5
        x[(1,1,4)] = 7.507e4
        x[(1,2,4)] = 1.338e4
        x[(2,0,4)] = 8.735e5
        x[(2,1,4)] = -1.657e5
        x[(3,0,4)] = -1.694e6
        #    x[(1,0,5)]=-920.9;x[(1,1,5)]=492.1;x[(1,2,5)]=135.0;x[(2,0,5)]=6742.;x[(2,1,5)]=-1053.;x[(3,0,5)]=-1.34e4
        x[(1,0,6)] = -8.898e5
        x[(1,1,6)] = 6.31e5
        x[(1,2,6)] = 5.068e4
        x[(2,0,6)] = 5.981e6
        x[(2,1,6)] = -1.415e6
        x[(3,0,6)] = -1.128e7
        x[(1,0,7)] = 8.696e5
        x[(1,1,7)] = -6.71e5
        x[(1,2,7)] = -3.008e4
        x[(2,0,7)] = -5.838e6
        x[(2,1,7)] = 1.514e6
        x[(3,0,7)] = 1.089e7
        Psi = lambda chi : [0,0,3715./756.,-16.*np.pi+113.*chi*(1./3.),15293365.0/508032.0-405.*chi**2/8.0,0,0,0]
        result = 1.
        v = (np.pi*M*f*GM_sun/c**3)**(1./3.) # dimensional less, total mass
        for k in range(2,8):
            sum_psi = Psi(chi)[k]
            for i in range(1,4):
                N = min(3-i,2);
                for j in range(0,N+1):  ### N -> N+1
                    sum_psi += x[(i,j,k)]*eta**i*chi**j
            result += sum_psi*v**k
        return 2.*np.pi*f*t0+phi0+3./128./eta/v**5*result

    def partial(self, A, m1, m2, chi, t0, phi0):
        """
        The matrix of partial derivatives of waveform as function of f

        Parameters:
          A (float or array of dtype float): The modulus of h(f)
          m1 (float): Red-shifted masses of the BHB
          m2 (float): Red-shifted masses of the BHB
          chi (float): spin
          t0 (float): The time of coalescence
          phi0 (float): The phase of coalescence

        Returns:
          (function): matrix of partial derivatives function of (f), Pij(f)
          f is array of float

        """
        delta = 1e-8

        phase_final = lambda f, m1, m2, chi, t0, phi0: self.phase(f, m1, m2, chi, t0, phi0)
        # part_A=lambda f: 1/A;
        # the error is determined with match-filtering of the waveform shape. therefore no derivative to the amplitude should be take.
        part_m1 = lambda f:(self.phase(f, m1+delta*m1, m2, chi, t0, phi0)-self.phase(f, m1-delta*m1, m2, chi, t0, phi0))/(2.*delta*m1)
        part_m2 = lambda f:(self.phase(f, m1, m2+delta*m2, chi, t0, phi0)-self.phase(f, m1, m2-delta*m2, chi, t0, phi0))/(2.*delta*m2)
        part_chi = lambda f:(self.phase(f, m1, m2, chi+delta, t0, phi0)-self.phase(f, m1, m2, chi-delta, t0, phi0))/(2.*delta)
        part_t0 = lambda f:2.*np.pi*f
        part_phi = lambda f:1.*np.ones(len(f))

        list_partial = lambda f: np.array([part_m1(f), part_m2(f), part_chi(f), part_t0(f), part_phi(f)])
        mat_part=lambda f: np.einsum('i...,j...->ij...',list_partial(f),list_partial(f))*self.mod_shape(f)**2*A**2
        #mat_part=lambda f: np.tensordot(list_partial(f),list_partial(f),axes=0)*self.mod_shape(f)**2*A**2
        #PartMat = np.zeros((5,5))
        #PartMat[(0,0)]=lambda f:1
        #for i in range(1,5):
        #    for j in range(i,5):
        #        PartMat[(i,j)]=lambda f: list[i]*list[j]*A**2
        #return lambda f,i,j:list_partial[i](f)*list_partial[j](f)*self.mod_shape(f)**2*A**2
        return mat_part

    def cos_mer_rate(self, z, m1, m2):
        """
        The fractional cosmic merger rate density of the stellar-mass BHB mergers.

        Parameters:
          z (float): The red-shift of the GW source
          m1 (float): Red-shifted masses of the primary BHB
          m2 (float): Red-shifted masses of the BHB
          # chi (float): effective spin

        Returns:
          (float): The number of mergers per year per Gpc3
        """
        m1=np.abs(m1)
        m2=np.abs(m2)
        z=np.abs(z)
        if self.pop=='I': # mass function = power law
        # it means we are using a different way to represent the cosmic merger rate, other than the ficuial parameterized way
            #R0, tau, skewness, loc, scale, q_low, self.chi_sigma = self.theta
            q=m2/m1
            result_part1=np.interp(z, self.zs, np.array(self.Rm))
            result_part2=PM1(m1, self.mu, self.c, self.gamma, self.mcut)
            #result_part3=PQ(q, self.q_low, self.mu, m1)
            result_part3=PQ(q, self.q_low, self.mu)
            #result_part4=np.exp(-0.5*(chi/self.chi_sigma)**2)/(np.sqrt(2.*np.pi)*self.chi_sigma)
            Jaccobian=1/m1
            ### Jaccobian of the transformation between coordinate (m1,m2)->(m1,q)
            #Jaccobian=1
            return Jaccobian*result_part1*result_part2*result_part3
        elif self.pop=='II': #mass function = power law + peak
            q=m2/m1
            result_part1=np.interp(z, self.zs, np.array(self.Rm))
            result_part2=PM2(m1, self.mu, self.c, self.gamma, self.mcut, self.mpeak, self.mpeak_scale, self.mpeak_sig)
            #result_part3=PQ(q, self.q_low, self.mu, m1)#
            result_part3=PQ(q, self.q_low, self.mu)
            #result_part4=np.exp(-0.5*(chi/self.chi_sigma)**2)/(np.sqrt(2.*np.pi)*self.chi_sigma)
            Jaccobian=1/m1
            ### Jaccobian of the transformation between coordinate (m1,m2)->(m1,q)
            #Jaccobian=1
            return Jaccobian*result_part1*result_part2*result_part3
        elif self.pop=='III': # z dependent mass function
            #print(len(self.theta))
        # the most complex way of formalization. Including alpha, beta, C in the Maudau-Dickinson, and z dependence of the mass functon parameters.
            q=m2/m1
            result_part1=np.interp(z, self.zs, np.array(self.Rm))
            mu_z=self.mu0+z*self.mu1
            c_z=self.c0+z*self.c1
            gamma_z=self.gamma0+z*self.gamma1
            ql_z=self.q0+z*self.q1
            result_part2=PM1(m1, mu_z, c_z, gamma_z, self.mcut)
            #result_part3=PQ(q, ql_z, self.mu_z, m1)
            result_part3=PQ(q, ql_z, self.mu_z)
            Jaccobian=1/m1
            return Jaccobian*result_part1*result_part2*result_part3
#        else:
#            #print(len(self.theta))
#            Mch = chirp_mass(m1,m2)
#            #eta = sym_ratio(m1,m2)
#            a0,a1,t0,t1,b0,b1,c0,c1,d0,d1 = self.theta
#
#        #    if (z<0 or z>=Z_HIGH or Mch<0):
#        #        result = 1e-10
#        #        norm = 1.
#        #        A = 1.
#        #        p_q = 1.
#        #        p_chi = 1.
#        #        Jaccobian=1
#        #    else:
#            t = self.cosmos.lookback_time(z).value #in unit of Gya
#            log10N = (a0+a1*t)/(np.exp((t-t0)/t1)+1.)
#            norm = 10**log10N
#                # the normalization
#            mu = b0+b1*t
#            sigL = c0+c1*t
#            sigR = d0+d1*t
#            A = np.sqrt(2./np.pi)/(sigL+sigR) # here is the problem
#            result=np.where(Mch<=mu,np.exp(-(mu-Mch)**2/(2.*sigL**2)),np.exp(-(Mch-mu)**2/(2.*sigR**2)))
#                # the distribution of chirpmass
#                #q = (1/eta-2-np.sqrt((1/eta-2)**2-4))/2.
#            q=m2/m1
#                # the mass ratio m2/m1 (<1).
#            sig_q = 0.2
#                # the width of distribution of q
#                #p_eta = np.exp(-(q-1)**2/(2.0*sig_q**2))
#                # the distribution of q, uniformly distributed
#            p_q=PQ(q, 1-sig_q)
#                #sig_chi = 0.01
#                # the widht of distribution of chi
#                #p_chi = np.exp(-chi**2/(2.0*sig_chi**2))/np.sqrt(2.0*np.pi)/sig_chi
#                #p_chi=np.exp(-0.5*(chi/sig_chi)**2)/(np.sqrt(2.*np.pi)*sig_chi)
#                # the distribution of chi
#                #Jaccobian=(m1*m2)**0.6*(m1+m2)**(-4.4)*((-m1+m2)*(0.2*m1*(m1 + m2)**0.2-0.6*(m1 + m2)**1.2) - (m1 - m2)*(0.2*m2*(m1 + m2)**0.2 - 0.6*(m1 + m2)**1.2))
#                ## the Jaccobian of the transformation (Mch,q)-->(m1,m2), which is easier to calculate.
#                #Jaccobian=1
#                #Jaccobian=0
#            Jaccobian=1.2*q*(m1*m2)**(-0.4)/(m1+m2)**0.2-m1**(-0.4)*m2**0.6*(1+q)*(m1+m2)**(-1.2)*0.2
#                #print("q=%f,m1=%f,m2=%f" % (q,m1,m2))
#            return result*norm*A*p_q*np.abs(Jaccobian)
            #return p_chi
                #return norm*A
            # asymmetric (split) Gaussian function.


    # def tel_fun(self, z, m1, m2, rho_cri, ant_fun, noise_tab, accurate=False):
    #     """
    #     The telescope function of Laser Interferometers and kHz sources.
    #
    #     Parameters:
    #       z (float): The redshift of the GW source
    #       m1 (float): Red-shifted masses of the BHB
    #       m2 (float): Red-shifted masses of the BHB
    #       #chi (float): spin
    #       rho_cri (float): The detection SNR threshold
    #       ant_fun (function): antenna pattern
    #       noise_tab (array of dtype float): noise function for detector
    #
    #     Returns:
    #       (float): The probability of detection
    #     """
    #     # both masses should be intrinsic here.
    #     Mch = chirp_mass(m1,m2)
    #     if accurate:
    #         path_angle_more=os.path.join(my_path, "accessory/angles_more.dat")
    #         random_angles_more=np.loadtxt(path_angle_more)
    #         theta_array_more = random_angles_more[:,0]
    #         varphi_array_more = random_angles_more[:,1]
    #         iota_array_more = random_angles_more[:,2]
    #         psi_array_more = random_angles_more[:,3]
    #         F = ant_fun(theta_array_more, varphi_array_more, psi_array_more)
    #         A_array = self.mod_norm(Mch*(1+z), F, iota_array_more, z)
    #     else:
    #         F = ant_fun(theta_array, varphi_array, psi_array)
    #         A_array = self.mod_norm(Mch*(1+z), F, iota_array, z)
    #     if np.isscalar(m1):
    #         f_up = self.freq_limit(m1=m1*(1+z), m2=m2*(1+z), chi=0)
    #         f2=self.freq_limit_merger(m1=m1*(1+z), m2=m2*(1+z), chi=0)
    #         f3=self.freq_limit_ringdown(m1=m1*(1+z), m2=m2*(1+z), chi=0)
    #         freq_sig=self.freq_sigma(m1=m1*(1+z), m2=m2*(1+z), chi=0)
    #     else :
    #         f_up = self.freq_limit(m1=m1*(1+z), m2=m2*(1+z), chi=np.zeros(len(m1)))
    #         f2=self.freq_limit_merger(m1=m1*(1+z), m2=m2*(1+z), chi=np.zeros(len(m1)))
    #     # the waveform want to eat red-shifted mass.
    #         f3=self.freq_limit_ringdown(m1=m1*(1+z), m2=m2*(1+z), chi=np.zeros(len(m1)))
    #         freq_sig=self.freq_sigma(m1=m1*(1+z), m2=m2*(1+z), chi=np.zeros(len(m1)))
    #     f1=f_up
    #     rho_sq_core_value = rho_sq_core(noise_tab, self.mod_shape, f_up=f_up)+rho_sq_core_merger(noise_tab, self.mod_shape_merger, f1=f1, f2=f2)+rho_sq_core_ringdown(noise_tab, self.mod_shape_ringdown,f1=f1, f2=f2, freq_sig=freq_sig, f3=f3)
    #
    #     #theta_array = np.arccos(np.random.uniform(low=0., high=1., size=length))
    #     #varphi_array = np.random.uniform(low=0., high=2.*np.pi, size=length)
    #     #iota_array = np.arccos(np.random.uniform(low=0., high=1., size=length))
    #     #psi_array = np.random.uniform(low=0., high=2.*np.pi, size=length)
    #     # an isotropic distribution of angles
    #
    #     if len(A_array.shape)==2:
    #         rho_sq_array=4.*np.einsum('i...,i->i...',A_array**2,rho_sq_core_value)
    #     #rho_sq_array = np.array(4.*A_array**2*rho_sq_core_value)
    #         heav_array = np.heaviside(rho_sq_array-rho_cri**2,0)
    #
    #         return np.mean(heav_array,axis=1)
    #     else:
    #         rho_sq_array = np.array(4.*A_array**2*rho_sq_core_value)
    #         heav_array = np.heaviside(rho_sq_array-rho_cri**2,0)
    #         return np.mean(heav_array)
        #return rho_sq_array
    def tel_fun(self, z, m1, m2, rho_cri, ant_fun, noise_tab, accurate=False, withangles=False):
        """
        The telescope function of Laser Interferometers and kHz sources.

        Parameters:
          z (float): The redshift of the GW source
          m1 (float): Red-shifted masses of the BHB
          m2 (float): Red-shifted masses of the BHB
          #chi (float): spin
          rho_cri (float): The detection SNR threshold
          ant_fun (function): antenna pattern
          noise_tab (array of dtype float): noise function for detector

        Returns:
          (float): The probability of detection
        """
        # both masses should be intrinsic here.
        Mch = chirp_mass(m1,m2)
        if accurate:
            path_angle_more=os.path.join(my_path, "accessory/angles_more.dat")
            random_angles_more=np.loadtxt(path_angle_more)
            theta_array_more = random_angles_more[:,0]
            varphi_array_more = random_angles_more[:,1]
            iota_array_more = random_angles_more[:,2]
            psi_array_more = random_angles_more[:,3]
            F = ant_fun(theta_array_more, varphi_array_more, psi_array_more)
            A_array = self.mod_norm(Mch*(1+z), F, iota_array_more, z)
        else:
            F = ant_fun(theta_array, varphi_array, psi_array)
            A_array = self.mod_norm(Mch*(1+z), F, iota_array, z)
        if np.isscalar(m1):
            f_up = self.freq_limit(m1=m1*(1+z), m2=m2*(1+z), chi=0)
            f2=self.freq_limit_merger(m1=m1*(1+z), m2=m2*(1+z), chi=0)
            f3=self.freq_limit_ringdown(m1=m1*(1+z), m2=m2*(1+z), chi=0)
            freq_sig=self.freq_sigma(m1=m1*(1+z), m2=m2*(1+z), chi=0)
        else :
            f_up = self.freq_limit(m1=m1*(1+z), m2=m2*(1+z), chi=np.zeros(len(m1)))
            f2=self.freq_limit_merger(m1=m1*(1+z), m2=m2*(1+z), chi=np.zeros(len(m1)))
        # the waveform want to eat red-shifted mass.
            f3=self.freq_limit_ringdown(m1=m1*(1+z), m2=m2*(1+z), chi=np.zeros(len(m1)))
            freq_sig=self.freq_sigma(m1=m1*(1+z), m2=m2*(1+z), chi=np.zeros(len(m1)))
        f1=f_up
        rho_sq_core_value = rho_sq_core(noise_tab, self.mod_shape, f_up=f_up)+rho_sq_core_merger(noise_tab, self.mod_shape_merger, f1=f1, f2=f2)+rho_sq_core_ringdown(noise_tab, self.mod_shape_ringdown,f1=f1, f2=f2, freq_sig=freq_sig, f3=f3)

        #theta_array = np.arccos(np.random.uniform(low=0., high=1., size=length))
        #varphi_array = np.random.uniform(low=0., high=2.*np.pi, size=length)
        #iota_array = np.arccos(np.random.uniform(low=0., high=1., size=length))
        #psi_array = np.random.uniform(low=0., high=2.*np.pi, size=length)
        # an isotropic distribution of angles

        if len(A_array.shape)==2:
            # in case of Bayesian inference on population model from GW catalogue
            rho_sq_array=4.*np.einsum('i...,i->i...',A_array**2,rho_sq_core_value)
        #rho_sq_array = np.array(4.*A_array**2*rho_sq_core_value)
            heav_array = np.heaviside(rho_sq_array-rho_cri**2,0)
            if withangles==True:
                #good_indice= np.argwhere(heav_array==1), self.chi_sigma = self.the
                #print(good_indice)
                #thechoice=np.random.choice(range(0,len(good_indice))
                #the_index=good_indice[thechoice][1]
                #print(the_index)
                #trans_heav=np.transpose(heav_array) # to randomize the angles
                #np.random.shuffle(trans_heav)  #
                #heav_array=np.transpose(trans_heav) #
                heav_array_fluffy=heav_array+np.random.normal(0,scale=1e-4,size=heav_array.shape) # here is a very smart trick, hope someone will appreciate.
                the_index=np.argmax(heav_array_fluffy,axis=1)
                thetheta=theta_array_more[the_index] if accurate else theta_array[the_index]
                thephi=varphi_array_more[the_index] if accurate else varphi_array[the_index]
                theiota=iota_array_more[the_index] if accurate else iota_array[the_index]
                thepsi=psi_array_more[the_index] if accurate else psi_array[the_index]
                therho2=np.diagonal(rho_sq_array[:,the_index])
                # index_bad=np.argwhere(therho2<rho_cri**2)
                # # deal with bad rho, it happens when the MCMC gives highly unlikely intrinsic parameters, and heav_array are all zero!
                # thetheta=np.delete(thetheta,index_bad)
                # thephi=np.delete(thephi, index_bad)
                # theiota=np.delete(theiota, index_bad)
                # thepsi=np.delete(thepsi, index_bad)
                # therho2=np.delete(therho2, index_bad)
                #print("my here! debugging")
                return [np.mean(heav_array,axis=1), thetheta, thephi, theiota, thepsi, therho2]
            else:
            #good_indice= np.where(heav_array==1)
            #np.random.choice(good_indice)
                return np.mean(heav_array,axis=1)
        else:
            # in case of MCMC sample of the GW synthetic catalogue
            rho_sq_array = np.array(4.*A_array**2*rho_sq_core_value)
            heav_array = np.heaviside(rho_sq_array-rho_cri**2,0)
            if withangles==True:
                good_indice= np.argwhere(heav_array==1)
                the_index=np.random.choice(good_indice)
                thetheta=theta_array_more[the_index] if accurate else theta_array[the_index]
                thephi=varphi_array_more[the_index] if accurate else varphi_array[the_index]
                theiota=iota_array_more[the_index] if accurate else iota_array[the_index]
                thepsi=psi_array_more[the_index] if accurate else psi_array[the_index]
                therho2=rho_sq_array[the_index]
                #print("my here! debugging")
                return [np.mean(heav_array), thetheta, thephi, theiota, thepsi, therho2]
            else:
                return np.mean(heav_array)
        #return rho_sq_array
    # def density_det(self, T, z, m1, m2, rho_cri, ant_fun, noise_tab,accurate):
    #     """
    #     The parameter distribution of detected sources.
    #
    #     Parameters:
    #       T (float): Observation time, in unit of minute
    #       z (array of floats): The redshift of the GW source, m1 and m2 should be in the same dimension with z
    #       m1 (array of floats): Red-shifted masses of the BHB
    #       m2 (array of floats): Red-shifted masses of the BHB
    #       chi (float): spin
    #       rho_cri (float): The detection SNR threshold
    #       ant_fun (function): antenna pattern
    #       noise_tab (array of dtype float): noise function for detector
    #
    #     Returns:
    #       (array of floats): Number density of detection, same length with z array.
    #     """
    #     T_year = (T*u.min).to(u.a).value # T in unit of minuts
    #     return 4.*np.pi*T_year*self.cos_mer_rate(z, m1, m2)*self.tel_fun(z,m1,m2, rho_cri,ant_fun,noise_tab,accurate)*self.cosmos.differential_comoving_volume(z).to_value(u.Gpc**3/u.sr)/(1+z)
    #     #return T_year*self.cos_mer_rate(z, m1, m2, chi)
    #     #return self.cosmos.differential_comoving_volume(z).to_value(u.Gpc**3/u.sr) 
    def density_det(self, T, z, m1, m2, rho_cri, ant_fun, noise_tab, accurate, withangles=False):
        """
        The parameter distribution of detected sources.

        Parameters:
          T (float): Observation time, in unit of minute
          z (array of floats): The redshift of the GW source, m1 and m2 should be in the same dimension with z
          m1 (array of floats): Red-shifted masses of the BHB
          m2 (array of floats): Red-shifted masses of the BHB
          chi (float): spin
          rho_cri (float): The detection SNR threshold
          ant_fun (function): antenna pattern
          noise_tab (array of dtype float): noise function for detector

        Returns:
          (array of floats): Number density of detection, same length with z array.
        """
        T_year = (T*u.min).to(u.a).value # T in unit of minuts
        return 4.*np.pi*T_year*self.cos_mer_rate(z, m1, m2)*self.tel_fun(z,m1,m2, rho_cri,ant_fun,noise_tab,accurate, withangles)*self.cosmos.differential_comoving_volume(z).to_value(u.Gpc**3/u.sr)/(1+z) # , self.cos_mer_rate(z, m1, m2), self.tel_fun(z,m1,m2, rho_cri,ant_fun,noise_tab,accurate, withangles)
        #return T_year*self.cos_mer_rate(z, m1, m2, chi)
        #return self.cosmos.differential_comoving_volume(z).to_value(u.Gpc**3/u.sr)

    def giveave_local(self,x):
        # Monte-Carlo integral with importance sampling
        i,length,T,rho_cri,ant_fun,noise_tab=x
#        np.random.seed(i*int(time.time()%3))
        z_array = z_array_ligo
        m1_array = m1_array_ligo
        m2_array = m2_array_ligo
        Ndet_array = self.density_det(T, z_array, m1_array, m2_array,rho_cri,ant_fun,noise_tab,accurate=False)/lognm(z_array,mu=-0.6,sig=0.4)/lognm(m1_array,mu=4,sig=1)/lognm(m2_array,mu=4,sig=1)/4.
        return np.mean(Ndet_array)

    def giveave_universe(self,x):
        i,length,T,rho_cri,ant_fun,noise_tab=x
        np.random.seed(i*int(time.time()%3))
        z_array=z_array_et
        m1_array=m1_array_et
        m2_array =m2_array_et
        Ndet_array = self.density_det(T, z_array, m1_array, m2_array,rho_cri,ant_fun,noise_tab,accurate=False)/lognm(z_array,mu=2,sig=1.2)/lognm(m1_array,mu=2.7,sig=0.5)/lognm(m2_array,mu=2.7,sig=0.5)
        return np.mean(Ndet_array)
    #chi_array = np.random.uniform(low=-0.5, high=0.5, size=length)

    def tot_num(self, T, rho_cri, ant_fun, noise_tab, generation):
        """
        The total number of sources detected.

        Parameters:
          T (float): Observation time, in unit of minutes
          rho_cri (float): The detection SNR threshold
          ant_fun (function): antenna pattern
          noise_tab (array of dtype float): noise function for detector
          ranges (list): parameter ranges

        Returns:
          (float): The total number of sources detected
        """
        #length = 10000
        #m1_ranges = ranges[1]
        #m2_ranges = ranges[2]
        #chi_ranges = ranges[3]
        #pool=Pool(4)
        #x1=[100,length,T,rho_cri,ant_fun,noise_tab]
        #x2=[200,length,T,rho_cri,ant_fun,noise_tab]
        #x3=[300,length,T,rho_cri,ant_fun,noise_tab]
        #x4=[400,length,T,rho_cri,ant_fun,noise_tab]
        if generation=='2G':
            # local sources
            #results=pool.map(self.giveave_local, [x1,x2,x3,x4])
            dnz=self.density_det(T, z_array_ligo, m1_array_ligo, m2_array_ligo, rho_cri, ant_fun, noise_tab,accurate=True)
            #sumation=0
            #for i in range(11):
            #    for j in range(53):
            #        for k in range(j+1):
            #            index=int(i*53*54/2+j*(j+1)/2+k)
            #            sumation+=dnz[index]*0.2*1*1 # 0.2*1*1 is the volume element in the parmaeter space
            sumation=np.sum(dnz)*0.2*1.8*1.8
            results=sumation
        elif generation=='3G':
            dnz=self.density_det(T, z_array_et, m1_array_et, m2_array_et, rho_cri, ant_fun, noise_tab,accurate=True)
            #sumation=0
            #for i in range(21):
            #    for j in range(53):
            #        for k in range(j+1):
            #            index=int(i*53*54/2+j*(j+1)/2+k)
            #            sumation+=dnz[index]*(10-1e-2)/20.*(55-3.01)/52.*(55-3.01)/52. # 1*1*1 is the volume element in the parmaeter space
            sumation=np.sum(dnz)*0.5*1*1
            results=sumation
        elif generation=='med':
            dnz=self.density_det(T, z_array_med, m1_array_med, m2_array_med, rho_cri, ant_fun, noise_tab,accurate=True)
            #sumation=0
            #for i in range(21):
            #    for j in range(53):
            #        for k in range(j+1):
            #            index=int(i*53*54/2+j*(j+1)/2+k)
            #            sumation+=dnz[index]*(10-1e-2)/20.*(55-3.01)/52.*(55-3.01)/52. # 1*1*1 is the volume element in the parmaeter space
            sumation=np.sum(dnz)*0.45*1.6*1.6
            results=sumation

            # the above is to calculate the total number at high redshift (z=6.72335754-10)
            #results=pool.map(self.giveave_universe, [x1,x2,x3,x4])
            #T_year=(T*u.min).to(u.a).value
            #Cosmology_1D=self.cosmos.differential_comoving_volume(self.zs[:40]).to_value(u.Gpc**3/u.sr)/(1.+self.zs[:40])
            #Nz=self.Rm[:40]*Cosmology_1D*4.*np.pi*T_year
            #results+=np.trapz(Nz,self.zs[:40])
        expect=results
        #return np.random.poisson(lam=expect)
        return expect

    def MCMCsample_Gibbs(self, n_sources, inits, ranges, T, rho_cri, ant_fun, noise_tab):
        """
            The parallel Markov-chain-Monte-Carlo sampling.
        """
        func=self.density_det
        n_cores=3
        n_sample=int(n_sources/n_cores)+1
        ps=[]
        for i in range(n_cores):
            p=[func, n_sample, inits, ranges, T, rho_cri, ant_fun, noise_tab, self.cosmos,i, self.chi_sigma]
            ps.append(p)
        pool=Pool(n_cores)
        traces=pool.map(mcmcunit, ps)
        # multiprocessing, parallel running with four cores.
        trace_all=np.concatenate(tuple(traces),axis=1)
        cata_all=trace_all[:,np.random.choice(np.arange(len(trace_all[0])),size=n_sources,replace=False)]
        pool.close()
        return cata_all
    def MCMCsample(self, n_sources, inits, T, rho_cri, ant_fun, noise_tab):
        """
            The parallel Markov-chain-Monte-Carlo sampling.
        """
        func=self.density_det
        n_cores=4
        n_sample=int(n_sources/n_cores)+1
        ps=[]
        for i in range(n_cores):
            p=[func, n_sample, inits, T, rho_cri, ant_fun, noise_tab, self.cosmos,i, self.chi_sigma]
            ps.append(p)
        pool=Pool(n_cores)
        traces=pool.map(mcmcunit_scout_bhbh, ps) # _old is the tranditional Metroplis-Hastling sampling, and w/o _old is Gibbs sampling.
        # multiprocessing, parallel running with three cores.
        trace_all=np.concatenate(tuple(traces),axis=1)
        cata_all=trace_all[:,np.random.choice(np.arange(len(trace_all[0])),size=n_sources,replace=False)]
        pool.close()
        return cata_all
    def MCMCsample_20april(self, n_sources, inits, T, rho_cri, ant_fun, noise_tab):
        """
            The parallel Markov-chain-Monte-Carlo sampling.
        """
        func=self.density_det
        n_cores=3
        n_sample=int(n_sources/n_cores)+1
        ps=[]
        for i in range(n_cores):
            p=[func, n_sample, inits, T, rho_cri, ant_fun, noise_tab, self.cosmos,i, self.chi_sigma]
            ps.append(p)
        pool=Pool(n_cores)
        traces=pool.map(mcmcunit_old, ps) # _old is the tranditional Metroplis-Hastling sampling, and w/o _old is Gibbs sampling.
        # multiprocessing, parallel running with three cores.
        trace_all=np.concatenate(tuple(traces),axis=1)
        cata_all=trace_all[:,np.random.choice(np.arange(len(trace_all[0])),size=n_sources,replace=False)]
        pool.close()
        return cata_all
    def MCMCsample_old(self, n_sources, inits, ranges, T, rho_cri, ant_fun, noise_tab):
        """
        The Markov-chain-Monte-Carlo sampling according to the distribution ndet(M, eta, z).

        Parameters:
          n_sources (int): number of sources to detect
          inits (list of floats): initial values of z, m1, m2, chi
          ranges (list of list of floats): parameter ranges
          rho_cri (float): The detection SNR threshold
          ant_fun (function): antenna pattern
          noise_tab (array of dtype float): noise function for detector

        Returns:
          (list of arrays of dtype float): samples of parameters Mchirp,z,m1,m2,chi,D

        """
        burning_steps = 100
        jump_steps = int(100/n_sources)+1

        z0,m10,m20,chi0 = inits
        step_z = 0.01
        step_m1 = 1.
        step_m2 = 1.
        step_chi = 0.1
        z_ranges = ranges[0]
        m1_ranges = ranges[1]
        m2_ranges = ranges[2]
        chi_ranges = ranges[3]
        # MCMC sampling according to distribution function(z,m1,m2)
        z,m1,m2,chi = [z0,m10,m20,chi0]
        # inital parameters
        length = 1
        samples_z = np.array([z])
        samples_m1 = np.array([m1])
        samples_m2 = np.array([m2])
        samples_chi = np.array([chi])

        while length < (n_sources*jump_steps+burning_steps):
            z_next,m1_next,m2_next,chi_next = [z,m1,m2,chi]+np.random.normal(scale=[step_z,step_m1,step_m2,step_chi],size=4)
            if z_ranges[0]<z_next<z_ranges[1] and m1_ranges[0]<m1_next<m1_ranges[1] and m2_ranges[0]<m2_next<m2_ranges[1] and chi_ranges[0]<chi_next<chi_ranges[-1]:
                p0 = self.density_det(T,z,m1,m2,chi,rho_cri,ant_fun,noise_tab, accurate=True)

                pac = min(1,self.density_det(T,z_next,m1_next,m2_next,chi_next,rho_cri,ant_fun,noise_tab,accurate=True)/p0) # accept probability

                if pac==1 or np.random.uniform(low=0.0, high=1.0, size=None) <= pac:
                    z,m1,m2,chi = [z_next,m1_next,m2_next,chi_next]
                    samples_z = np.append(samples_z,[z])
                    samples_m1 = np.append(samples_m1,[max(m1,m2)])
                    samples_m2 = np.append(samples_m2,[min(m1,m2)])
                    samples_chi = np.append(samples_chi,[chi])
                    length += 1

        samples_D = self.cosmos.luminosity_distance(samples_z).value
        samples_Mc = chirp_mass(samples_m1,samples_m2)

        samples_Mc_short=samples_Mc[burning_steps::jump_steps]
        samples_z_short=samples_z[burning_steps::jump_steps]
        samples_m1_short=samples_m1[burning_steps::jump_steps]
        samples_m2_short=samples_m2[burning_steps::jump_steps]
        samples_chi_short=samples_chi[burning_steps::jump_steps]
        samples_D_short=samples_D[burning_steps::jump_steps]
        cat=[samples_Mc_short,samples_z_short,samples_m1_short,samples_m2_short,samples_chi_short,samples_D_short]

        tac=np.transpose(cat)
        np.random.shuffle(tac)
        return np.transpose(tac)

    def errors_FIM(self, n_sources, samples, noise_tab):
        """
        Return errors of parameters from Fisher Information Matrix

        Parameters:
          n_sources (int): number of sources to detect
          samples (list of arrays of dtype float): sampled parameters
          noise_tab (array of dtype float): noise function for detector

        Returns:
          (list of arrays of dtype float): errors of sampled parameters m1,m2,chi
        """
        errors_m1 = np.zeros(n_sources)
        errors_m2 = np.zeros(n_sources)
        errors_chi = np.zeros(n_sources)

        for i in range(0,n_sources):
            #print("dealing with %d-th source" % i)
            z = samples[1][i]
            m1 = samples[2][i]
            m2 = samples[3][i]
            Mch = samples[0][i]
            DL = self.cosmos.luminosity_distance(z).to_value(u.Gpc)
            A = CONST_AMPLITUDE_GW*(Mch*(1.+z))**(5./6.)/DL
            chi = samples[4][i]

            part_mat = self.partial(A,(1.+z)*m1,(1.+z)*m2,chi,0,0)
            f_up = self.freq_limit((1.+z)*m1,(1.+z)*m2,chi)
            fim = fis_inf_matr(part_mat,noise_tab,f_up=f_up,numpar=5)
            err_mt = errors(fim)
            # Covariance Matrix, the inverse matrix of the FIM.

            #ErrMt_m1m2=ErrMt[np.ix_([0,1],[0,1])]
            #conv = FIM_conv_matr(m1,m2,5)
            #err_mt_tilde = np.dot(np.dot(conv.transpose(),err_mt),conv)
            errors_m1[i] = max(min(np.sqrt(np.diag(err_mt)[0]),0.5*m1), 0.05*m1)
            errors_m2[i] = max(min(np.sqrt(np.diag(err_mt)[1]),0.5*m2), 0.05*m2)
            errors_chi[i] = np.sqrt(np.diag(err_mt)[2])

        return [errors_m1,errors_m2,errors_chi]
class DNS(BHB):
    """
    This is a class to describe double neutron stars mergers.
    It inherits all functions from BHB class except set_model_theta and cos_mer_rate.

    Attributes:
    cosmos: define cosmological model

    """

    def __init__(self,cosmos):
        """
        Parameters:
          cosmos (class): define cosmological model
        """
        self.cosmos = cosmos
        #self.theta = thetaDNS
        #self.chi_sigma=0.1
        self.zs=np.linspace(1e-2,10,100)
        #R0, tau, loc,scal,low,high = self.theta
        #self.zs=np.linspace(1e-2,10,100)
        #self.Rm=np.zeros(len(self.zs))
        #self.Rm=R0*R(self.zs, 2.7, 5.6, 2.9, tau, self.cosmos)
    def set_model_theta(self, new_theta=None):
        """
        The function to change theta from fiducial to user-defined.

        Parameters:
          new_theta (Optional[list of floats]): new parameter values

        Returns:
          (list of floats): theta with new values, if new_theta=None return theta to fiducial
        """
        if new_theta != None:
           self.theta = new_theta
        else:
           self.theta = DNS_Pop1
        R0, tau, self.loc, self.scal,self.low,self.high, self.chi_sigma = self.theta
        if not R0>0:
            raise ValueError("R0 must be positive")
        if not 0.1<tau<100:
            raise ValueError("tau should be limited between 0.1-100")
        if not self.low>0:
            raise ValueError("m_low must be positive")
        if not self.high>self.low:
            raise ValueError("m_high must be larger than m_low")
        if not self.low<self.loc<self.high:
            raise ValueError("m_peak must in between m_low and m_high")
        if not self.scal>0:
            raise ValueError("m_scale must be positive")
        if not self.chi_sigma>0:
            raise ValueError("chi_sigma must be positive")
        self.Rm=R0*R(self.zs, 2.7, 5.6, 2.9, tau, self.cosmos)
    def cos_mer_rate(self, z, m1, m2):
        """
        The cosmic merger rate density of the stellar-mass DNS mergers.

        Parameters:
          z (float): The redshift of the GW source
          m1 (float): Red-shifted masses of the NS
          m2 (float): Red-shifted masses of the NS
          #chi (float): spin

        Returns:
          (float): The number of mergers per year per Gpc3
        """
        #a0,a1,t0,t1,loc,scal,low,high = self.theta
        #R0, tau, loc,scal,low,high = self.theta
        #if (z<=0 or z>=Z_HIGH): rate = 1e-10
        #else:
        #t = self.cosmos.lookback_time(z).value
        #log10N = (a0+a1*t)/(np.exp((t-t0)/t1)+1.)
        #norm = 10**log10N
            # the normalization
        norm=np.interp(z, self.zs, np.array(self.Rm))
        aNS,bNS = (self.low-self.loc)/self.scal, (self.high-self.loc)/self.scal
        pm1 = truncnorm.pdf(m1, aNS, bNS, loc=self.loc, scale=self.scal)
        pm2 = truncnorm.pdf(m2, aNS, bNS, loc=self.loc, scale=self.scal)
            #chi_sigma=0.1
            #pchi=np.exp(-0.5*(chi/chi_sigma)**2)/(np.sqrt(2.*np.pi)*chi_sigma)
            # the distribution of m1 and m2.
        rate = norm*pm1*pm2
        return rate

    def giveave_local(self,x):
        a0,a1,t0,t1,loc,scal,low,high = self.theta
        aNS,bNS = (low-loc)/scal, (high-loc)/scal
        #pm1 = truncnorm.pdf(m1, aNS, bNS, loc=loc, scale=scal)
        i,length,T,rho_cri,ant_fun,noise_tab=x
        np.random.seed(i*int(time.time()%3))
        z_array = np.random.lognormal(-1.4,1.2,size=length)
        m1_array= truncnorm.rvs(aNS, bNS, loc=loc, scale=scal,size=length)
        m2_array= truncnorm.rvs(aNS, bNS, loc=loc, scale=scal,size=length)
        #m1_array = np.random.lognormal(2.7,0.5,size=length)
        #m2_array = np.random.lognormal(2.7,0.5,size=length)
        Ndet_array = np.array([self.density_det(T, z, m1, m2,rho_cri,ant_fun,noise_tab,accurate=True)/lognm(z,mu=-1.4,sig=1.2)/truncnorm.pdf(m1, aNS, bNS, loc=loc, scale=scal)/truncnorm.pdf(m2, aNS, bNS, loc=loc, scale=scal) for (z, m1, m2) in zip(z_array, m1_array, m2_array)])
        return np.mean(Ndet_array)

    def giveave_universe(self,x):
        a0,a1,t0,t1,loc,scal,low,high = self.theta
        aNS,bNS = (low-loc)/scal, (high-loc)/scal
        i,length,T,rho_cri,ant_fun,noise_tab=x
        np.random.seed(i*int(time.time()%3))
        z_array = np.random.lognormal(0.69,1.2,size=length)
        m1_array= truncnorm.rvs(aNS, bNS, loc=loc, scale=scal, size=length)
        m2_array= truncnorm.rvs(aNS, bNS, loc=loc, scale=scal, size=length)
        Ndet_array = np.array([self.density_det(T, z, m1, m2,rho_cri,ant_fun,noise_tab,accurate=False)/lognm(z,mu=0.69,sig=1.2)/truncnorm.pdf(m1, aNS, bNS, loc=loc, scale=scal)/truncnorm.pdf(m2, aNS, bNS, loc=loc, scale=scal) for (z, m1, m2) in zip(z_array, m1_array, m2_array)])
        return np.mean(Ndet_array)

    def tot_num(self, T, rho_cri, ant_fun, noise_tab, generation):
        #z_ranges = ranges[0]
        #m1_ranges = ranges[1]
        #m2_ranges = ranges[2]
        #chi_ranges = ranges[3]
        #x=1,1000,T,rho_cri,ant_fun,noise_tab
        if generation=='2G':
            #results=pool.map(self.giveave_local, [x1,x2,x3,x4])
            dnz=self.density_det(T, z_array_ligo_DNS, m1_array_ligo_DNS, m2_array_ligo_DNS, rho_cri, ant_fun, noise_tab,accurate=True)
            #sumation=0
            #for i in range(11):
            #    for j in range(21):
            #        for k in range(j+1):
            #            index=int(i*21*22/2+j*(j+1)/2+k)
            #            sumation+=dnz[index]*(1e-2-1e-4)/10.*(2.5-1)/20.*(2.5-1)/20. # 0.2*1*1 is the volume element in the parmaeter space
            sumation=np.sum(dnz)*(1e-1-1e-4)/10.*(2.5-1)/20.*(2.5-1)/20.
            results=sumation
        elif generation=='3G':
            dnz=self.density_det(T, z_array_et_DNS, m1_array_et_DNS, m2_array_et_DNS, rho_cri, ant_fun, noise_tab,accurate=True)
            #sumation=0
            #for i in range(11):
            #    for j in range(21):
            #        for k in range(j+1):
            #            index=int(i*21*22/2+j*(j+1)/2+k)
            #            sumation+=dnz[index]*(5-1e-2)/10.*(2.5-1)/20.*(2.5-1)/20. # 1*1*1 is the volume element in the parmaeter space
            sumation=np.sum(dnz)*(5-1e-2)/10.*(2.5-1)/20.*(2.5-1)/20.
            results=sumation
        else:
            dnz=self.density_det(T, z_array_med_DNS, m1_array_med_DNS, m2_array_med_DNS, rho_cri, ant_fun, noise_tab,accurate=True)
            #sumation=0
            #for i in range(11):
            #    for j in range(21):
            #        for k in range(j+1):
            #            index=int(i*21*22/2+j*(j+1)/2+k)
            #            sumation+=dnz[index]*(5-1e-2)/10.*(2.5-1)/20.*(2.5-1)/20. # 1*1*1 is the volume element in the parmaeter space
            sumation=np.sum(dnz)*(0.5-1e-4)/10.*(2.5-1)/20.*(2.5-1)/20.
            results=sumation
        #if z_ranges[1]<=3:
        #    result=self.giveave_local(x)
        #else:
        #    result=self.giveave_universe(x)
        #return np.random.poisson(lam=results)
        return results
    def MCMCsample(self, n_sources, inits, T, rho_cri, ant_fun, noise_tab):
        """
            The parallel Markov-chain-Monte-Carlo sampling.
            DNS
        """
        func=self.density_det
        n_cores=3
        if n_sources<=10:
            n_larger=50*n_sources
        else:
            n_larger=n_sources
        n_sample=int(n_larger/n_cores)+1
        ps=[]
        for i in range(n_cores):
            p=[func, n_sample, inits,T,rho_cri, ant_fun, noise_tab, self.cosmos,i*100, self.chi_sigma]
            ps.append(p)
        pool=Pool(n_cores)
        traces=pool.map(mcmcunit_scout_bhbh, ps) # _old is the tranditional Metroplis-Hastling sampling, and w/o _old is Gibbs sampling.
        # multiprocessing, parallel running with three cores.
        trace_all=np.concatenate(tuple(traces),axis=1)
        cata_all=trace_all[:,np.random.choice(np.arange(len(trace_all[0])),size=n_sources,replace=False)]
        pool.close()
        return cata_all
class BHNS(BHB):
    """
    This is a class to describe stellar mass black hole neutron stars mergers.
    It inherits all functions from BHB class except set_model_theta and cos_mer_rate.

    Attributes:
    cosmos: define cosmological model

    """

    def __init__(self, cosmos):
        """
        Parameters:
          cosmos (class): define cosmological model
        """
        self.cosmos = cosmos
        #self.theta = thetaBHNS
        self.zs=np.linspace(1e-2,10,100)
        self.Rm= np.zeros(len(self.zs))
        #self.chi_sigma=0.1

    def set_model_theta(self, pop, new_theta=None):
        """
        The function to change theta from fiducial to user-defined.

        Parameters:
          new_theta (Optional[list of floats]): new parameter values

        Returns:
          (list of floats): theta with new values, if new_theta=None return theta to fiducial
        """
        if pop=='I':
            if new_theta != None:
                self.theta = new_theta
            else:
                self.theta = BHNS_Pop1
            R0, tau, self.loc,self.scal,self.low,self.high, self.mu, self.c, self.gamma, self.mcut, self.chi_sigma = self.theta
            if not R0>0:
                raise ValueError("R0 should be positive.")
            if not 0.1<tau<100:
                raise ValueError("tau should be limited between 0.1-100")
            if not self.low>0:
                raise ValueError("m_low should be positive")
            if not self.high>self.low:
                raise ValueError("m_high should be larger than m_low")
            if not self.low<self.loc<self.high:
                raise ValueError("m_peak should in between m_low and m_high")
            if not 0<self.mu:
                raise ValueError("mu needs to be positive.")
            if not self.c>0:
                raise ValueError("c should be larger than zero")
            if not self.gamma>1:
                raise ValueError("gamma should >1, otherwise can't normalise.")
            if not self.mcut>self.c/self.gamma+self.mu:
                raise ValueError("mcut should be larger than c/gamma+mu")
            if not self.chi_sigma>0:
                raise ValueError("chi_sigma should be larger than zero")
        elif pop=='II':
            if new_theta != None:
                self.theta = new_theta
            else:
                self.theta = BHNS_Pop2
            R0, tau, self.loc,self.scal,self.low,self.high, self.mu, self.c, self.gamma, self.mcut, self.m_peak, self.m_peak_scale, self.m_peak_sig, self.chi_sigma = self.theta
            if not self.m_peak>0:
                raise ValueError("m_peak should be positive")
            if not self.m_peak_sig:
                raise ValueError("m_peak_sig should be positive")
            if not R0>0:
                raise ValueError("R0 should be positive.")
            if not 0.1<tau<100:
                raise ValueError("tau should be limited between 0.1-100")
            if not self.low>0:
                raise ValueError("m_low should be positive")
            if not self.high>self.low:
                raise ValueError("m_high should be larger than m_low")
            if not self.low<self.loc<self.high:
                raise ValueError("m_peak should in between m_low and m_high")
            if not 0<self.mu:
                raise ValueError("mu needs to be positive.")
            if not self.c>0:
                raise ValueError("c should be larger than zero")
            if not self.gamma>1:
                raise ValueError("gamma should >1, otherwise can't normalise.")
            if not self.mcut>self.c/self.gamma+self.mu:
                raise ValueError("mcut should be larger than c/gamma+mu")
            if not self.chi_sigma>0:
                raise ValueError("chi_sigma should be larger than zero")
        self.Rm=R0*R(self.zs, 2.7, 5.6, 2.9, tau, self.cosmos)
        self.pop=pop
    def cos_mer_rate(self, z, M, m):
        """
        The cosmic merger rate density of the stellar-mass BHB mergers.

        Parameters:
          z (float): The redshift of the GW source
          M (float): Red-shifted mass of the BH
          m (float): Red-shifted mass of the NS
          #chi (float): spin

        Returns:
          (float): The number of mergers per year per Gpc3
        """
        #R0, tau, loc,scal,low,high, mu, c, gamma, mcut = self.theta

        #if (z<=0 or z>=Z_HIGH or M<0 or m<0): rate = 1e-10

        #t = self.cosmos.lookback_time(z).value
        #log10N = (a0+a1*t)/(np.exp((t-t0)/t1)+1.)
        norm = np.interp(z, self.zs, np.array(self.Rm))
            # the normalization
        aNS,bNS = (self.low-self.loc)/self.scal, (self.high-self.loc)/self.scal
        pm = truncnorm.pdf(m, aNS, bNS, loc=self.loc, scale=self.scal)
        if self.pop=='I':
            pM = PM1(M, self.mu, self.c, self.gamma, self.mcut)
        elif self.pop=='II':
            pM = PM2(M, self.mu, self.c, self.gamma, self.mcut, self.m_peak, self.m_peak_scale, self.m_peak_sig)
            # the mass of neutron star
        #mu = b0+b1*z
        #sigL = c0+c1*t
        #sigR = d0+d1*t
        #A = np.sqrt(2./np.pi)/(sigL+sigR)
        #pM=np.where(M<=mu, np.exp(-(mu-M)**2/(2.*sigL**2)), np.exp(-(M-mu)**2/(2.*sigR**2)))
                    # the distribution of BH mass
            #chi_sigma=0.1
            #pchi =np.exp(-0.5*(chi/chi_sigma)**2)/(np.sqrt(2.*np.pi)*chi_sigma)
        rate = norm*pm*pM
        return rate

    def giveave_local(self,x):
        a0,a1,t0,t1,loc,scal,low,high,b0,b1,c0,c1,d0,d1 = self.theta
        aNS,bNS = (low-loc)/scal, (high-loc)/scal
        #pm1 = truncnorm.pdf(m1, aNS, bNS, loc=loc, scale=scal)
        i,length,T,rho_cri,ant_fun,noise_tab=x
        np.random.seed(i*int(time.time()%3))
        z_array = np.random.lognormal(-1.4,1.2,size=length)
        M_array= np.random.lognormal(2.7,0.5,size=length)
        m_array= truncnorm.rvs(aNS, bNS, loc=loc, scale=scal,size=length)
        #m1_array = np.random.lognormal(2.7,0.5,size=length)
        #m2_array = np.random.lognormal(2.7,0.5,size=length)
        Ndet_array = np.array([self.density_det(T, z, M, m,rho_cri,ant_fun,noise_tab,accurate=False)/lognm(z,mu=-1.4,sig=1.2)/truncnorm.pdf(m, aNS, bNS, loc=loc, scale=scal)/lognm(M,mu=2.7,sig=0.5) for (z, M, m) in zip(z_array, M_array, m_array)])
        return np.mean(Ndet_array)

    def giveave_universe(self,x):
        a0,a1,t0,t1,loc,scal,low,high,b0,b1,c0,c1,d0,d1 = self.theta
        aNS,bNS = (low-loc)/scal, (high-loc)/scal
        i,length,T,rho_cri,ant_fun,noise_tab=x
        np.random.seed(i*int(time.time()%3))
        z_array = np.random.lognormal(0.69,1.2,size=length)
        M_array= np.random.lognormal(2.7,0.5,size=length)
        m_array= truncnorm.rvs(aNS, bNS, loc=loc, scale=scal,size=length)
        Ndet_array = np.array([self.density_det(T, z, M, m,rho_cri,ant_fun,noise_tab,accurate=False)/lognm(z,mu=0.69,sig=1.2)/truncnorm.pdf(m, aNS, bNS, loc=loc, scale=scal)/lognm(M,mu=2.7,sig=0.5) for (z, M, m) in zip(z_array, M_array, m_array)])
        return np.mean(Ndet_array)


    def tot_num(self, T, rho_cri, ant_fun, noise_tab, generation):
#        z_ranges = ranges[0]
#        m1_ranges = ranges[1]
#        m2_ranges = ranges[2]
#        chi_ranges = ranges[3]
        #x=1,1000,T,rho_cri,ant_fun,noise_tab
        #if z_ranges[1]<=3:
        #    result=self.giveave_local(x)
        #else:
        #    result=self.giveave_universe(x)
        if generation=='2G':
            #results=pool.map(self.giveave_local, [x1,x2,x3,x4])
            dnz=self.density_det(T, z_array_ligo_BHNS, m1_array_ligo_BHNS, m2_array_ligo_BHNS, rho_cri, ant_fun, noise_tab,accurate=True)
            sumation=np.sum(dnz)*0.2*(2.5-1)/20.*1
            results=sumation
        elif generation=='3G':
            dnz=self.density_det(T, z_array_et_BHNS, m1_array_et_BHNS, m2_array_et_BHNS, rho_cri, ant_fun, noise_tab,accurate=True)
            #sumation=0
            #for i in range(11):
            #    for j in range(53):
            #        for k in range(21):
            #            index=i*21*53+j*21+k
            #            sumation+=dnz[index]*(10-1e-2)/10.*(2.5-1)/20.*(55-3.01)/52. # 1*1*1 is the volume element in the parmaeter space
            sumation=np.sum(dnz)*(10-1e-2)/10.*(2.5-1)/20.*(55-3.01)/52.
            results=sumation
        else:
            dnz=self.density_det(T, z_array_med_BHNS, m1_array_med_BHNS, m2_array_med_BHNS, rho_cri, ant_fun, noise_tab,accurate=True)
            #sumation=0
            #for i in range(11):
            #    for j in range(53):
            #        for k in range(21):
            #            index=i*21*53+j*21+k
            #            sumation+=dnz[index]*(10-1e-2)/10.*(2.5-1)/20.*(55-3.01)/52. # 1*1*1 is the volume element in the parmaeter space
            sumation=np.sum(dnz)*0.2*(2.5-1)/20.*60./52.
            results=sumation
        #return np.random.poisson(lam=results)
        return results

    def MCMCsample(self, n_sources, inits, T, rho_cri, ant_fun, noise_tab):
        """
            The parallel Markov-chain-Monte-Carlo sampling.
        """
        func=self.density_det
        if n_sources<=10:
            n_larger=50*n_sources
        else:
            n_larger=n_sources
        n_cores=8 # in desktop
        n_sample=int(n_larger/n_cores)+1
        ps=[]
        for i in range(n_cores):
            p=[func, n_sample, inits, T, rho_cri, ant_fun, noise_tab, self.cosmos,i, self.chi_sigma]
            ps.append(p)
        pool=Pool(n_cores)
        traces=pool.map(mcmcunit_scout_bhbh, ps) # _old is the tranditional Metroplis-Hastling sampling, and w/o _old is Gibbs sampling.
        # multiprocessing, parallel running with three cores.
        trace_all=np.concatenate(tuple(traces),axis=1)
        cata_all=trace_all[:,np.random.choice(np.arange(len(trace_all[0])),size=n_sources,replace=False)]
        pool.close()
        return cata_all
class Background(DNS):
    """
    This is the source population originated from the background noises. (fake signals)
    """
    def __init__(self, cosmos):
        """
        Parameters:
          cosmos (class): define cosmological model
        """
        self.cosmos = cosmos
        #self.theta = thetaBHB
        #self.zs= np.logspace(-4, 1., 30)
        self.zs=np.linspace(1e-2,10,100)
        #self.Rm= np.zeros(len(self.zs))
        #self.chi_sigma=0.1
        self.pop='DNS'

    def set_model_theta(self, pop, new_theta=None):
        if not pop in ['DNS']:
            raise ValueError("Now pop only works for DNS");
        if pop=='DNS':
            self.m_low=0.5
            self.m_high=3
            self.chi_sigma=DNS_Pop1[-1]
        elif pop=='BHB':
            self.m_low=3
            self.m_high=60

        if new_theta==None and pop=='DNS':
            self.theta=BG_DNS
            self.chi_sigma=DNS_Pop1[-1]
        elif new_theta==None and pop=='BHB':
            self.theta=BG_BBH
        else:
            self.theta=new_theta

    def R(self, z):
        """
        event rate as function of red-shift.
        z can be float or also nparray.
        """
        Rn=self.theta[0]
        alpha=self.theta[1]
        D_ref=self.theta[2] # Mpc
        D=self.cosmos.luminosity_distance(z).value
        P=Rn*np.exp(-(D_ref/D-1)/alpha)*(D_ref/D**2)*dDovdz(z, self.cosmos)
        Rate=P*(1+z)/self.cosmos.differential_comoving_volume(z).to_value(u.Gpc**3/u.sr)/(4.*np.pi)
        return Rate

    def massfunction(self, m):
        """
        event rate as function of masses. (the same for both components)
        """
        return np.where((m>self.m_low) * (m<self.m_high), 1./(self.m_high-self.m_low), 0)

    def cos_mer_rate(self, z, m1, m2):
        """
        inferred rate of fake signal as function of z, m1, m2
        """
        rate=self.R(z)*self.massfunction(m1)*self.massfunction(m2)
        return rate

    def tot_num(self, T, rho_cri, ant_fun, noise_tab, generation):
        """
        The total number of sources detected.

        Parameters:
          T (float): Observation time, in unit of minutes
          rho_cri (float): The detection SNR threshold
          ant_fun (function): antenna pattern
          noise_tab (array of dtype float): noise function for detector
          ranges (list): parameter ranges

        Returns:
          (float): The total number of sources detected
        """
        para_IS_bg=np.loadtxt(path_IS_ligo_BGDNS)
        z_array_bg = para_IS_bg[:,0]
        m1_array_bg = para_IS_bg[:,1]
        m2_array_bg = para_IS_bg[:,2]
        dnz=self.density_det(T, z_array_bg, m1_array_bg, m2_array_bg, rho_cri, ant_fun, noise_tab,accurate=True)*z_array_bg
        #sumation=0
        #for i in range(11):
        #    for j in range(53):
        #        for k in range(j+1):
        #            index=int(i*53*54/2+j*(j+1)/2+k)
        #            sumation+=dnz[index]*0.2*1*1 # 0.2*1*1 is the volume element in the parmaeter space
        sumation=np.sum(dnz)*(np.log(5)-np.log(1e-2))/40*((3-0.5)/20)**2 # integrating in ln z* m1*m2 evently grids space.
        results=sumation
        return results

    # def MCMCsample(self, n_sources, inits, T, rho_cri, ant_fun, noise_tab):
    #     """
    #         The parallel Markov-chain-Monte-Carlo sampling.
    #     """
    #     func=self.density_det
    #     if n_sources<=10:
    #         n_larger=50*n_sources
    #     else:
    #         n_larger=n_sources
    #     n_cores=8 # in desktop
    #     n_sample=int(n_larger/n_cores)+1
    #     ps=[]
    #     for i in range(n_cores):
    #         p=[func, n_sample, inits, T, rho_cri, ant_fun, noise_tab, self.cosmos,i, self.chi_sigma]
    #         ps.append(p)
    #     pool=Pool(n_cores)
    #     traces=pool.map(mcmcunit_old, ps) # _old is the tranditional Metroplis-Hastling sampling, and w/o _old is Gibbs sampling.
    #     # multiprocessing, parallel running with three cores.
    #     trace_all=np.concatenate(tuple(traces),axis=1)
    #     cata_all=trace_all[:,np.random.choice(np.arange(len(trace_all[0])),size=n_sources,replace=False)]
    #     pool.close()
    #     return cata_all
