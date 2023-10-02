import pandas as pd, numpy as np
from gwtoolbox.functions_earth import *
from pycbc import waveform
class fisher:
    def __init__(self, det, approximant, cosmos):
        """
        det is the detector class
        approximant is str, describing the approximant of the waveform template
        """
        self.det=det
        self.approximant=approximant
        self.cosmos=cosmos
    def response(self, kwargs):
        """
        kwargs is a dict of parameters
        keys of kwargs (9): m1, m2, chi, D, inc, theta, varphi, psi, phi0
        """
        theta=np.arctan(kwargs['tan_theta'])+0.5*np.pi
        varphi=np.arctan(kwargs['tan_varphi'])+0.5*np.pi
        psi=2*(np.arctan(kwargs['tan_psi'])+0.5*np.pi)
        #D_lumi=10**kwargs['logD']
        D_lumi=kwargs['D']
        z=zofD(D_lumi, self.cosmos)
        hpf, htf = waveform.waveform.get_fd_waveform(
            mass1=kwargs['m1']*(1+z),
            mass2=kwargs['m2']*(1+z),
            spin1z=kwargs['χ'],
            spin2z=kwargs['χ'],
            distance=D_lumi,#kwargs['D'], # in Mpc
            inclination=np.arctan(kwargs['tan_inc'])+0.5*np.pi,
            approximant=self.approximant,
            f_lower=1,
            delta_f=1, #
            coa_phase = 2*(np.arctan(kwargs['tan_phi0'])+0.5*np.pi)
        )

        fp, ft=self.det.ante_pattern(
            theta=theta,
            varphi=varphi,
            psi=psi
#             theta=np.arctan(kwargs['tan_theta'])+0.5*np.pi,
#             varphi=np.arctan(kwargs['tan_varphi'])*0.5*np.pi,
#             psi=2*(np.arctan(kwargs['tan_psi'])+0.5*np.pi)
        )

        hres=hpf*fp+htf*ft # its a one-d np.array type complex number. The index of it divided by delta_f is the real frequency in Hz
        return hres

    def partial_know_toomuch(self, kwargs):
        delta=1e-10;

        keys_topar=['m1', 'm2', 'χ', 'D','tan_inc']
        part_list=[]
        for key in keys_topar:
            kwargs_right=kwargs.copy()
            kwargs_left=kwargs.copy()
            if not kwargs[key]==0:
                kwargs_right[key]*=(1+delta)
                kwargs_left[key]*=(1-delta)
                hres_right=self.response(kwargs_right)
                hres_left =self.response(kwargs_left)
                part=(hres_right-hres_left)/(2*kwargs[key]*delta)
            else:
                kwargs_right[key]+=delta
                kwargs_left[key]-=delta
                hres_right=self.response(kwargs_right)
                hres_left =self.response(kwargs_left)
                part=(hres_right-hres_left)/(2*delta)
            #if key=='inc':
            #print(part)
            #part=np.where(np.abs(hres_right-hres_left)>1e-10,(hres_right-hres_left)/(2*kwargs[key]),1e-10/(2*kwargs[key])) # to prevent singular matrix
            # part is np.array of complex number
            part_list.append(part)
        part_nparray=np.array(part_list) # [7*dim(f)]
        mat_part=np.einsum('i..., j...-> ij...', np.conj(part_nparray), part_nparray) # [7*7*dim(f)]
        #self.mat_part=mat_part
        return mat_part

    def partial_know_loc(self, kwargs):
        delta=1e-10;

        keys_topar=['m1', 'm2', 'χ', 'D', 'tan_psi', 'tan_phi0', 'tan_inc']
        part_list=[]
        for key in keys_topar:
            kwargs_right=kwargs.copy()
            kwargs_left=kwargs.copy()
            if not kwargs[key]==0:
                kwargs_right[key]*=(1+delta)
                kwargs_left[key]*=(1-delta)
                hres_right=self.response(kwargs_right)
                hres_left =self.response(kwargs_left)
                part=(hres_right-hres_left)/(2*kwargs[key]*delta)
            else:
                kwargs_right[key]+=delta
                kwargs_left[key]-=delta
                hres_right=self.response(kwargs_right)
                hres_left =self.response(kwargs_left)
                part=(hres_right-hres_left)/(2*delta)
            #if key=='inc':
            #print(part)
            #part=np.where(np.abs(hres_right-hres_left)>1e-10,(hres_right-hres_left)/(2*kwargs[key]),1e-10/(2*kwargs[key])) # to prevent singular matrix
            # part is np.array of complex number
            part_list.append(part)
        part_nparray=np.array(part_list) # [7*dim(f)]
        mat_part=np.einsum('i..., j...-> ij...', np.conj(part_nparray), part_nparray) # [7*7*dim(f)]
        #self.mat_part=mat_part
        return mat_part

    def partial(self, kwargs):
        delta=1e-10;

        keys_topar=['m1', 'm2', 'χ', 'D','tan_psi', 'tan_phi0', 'tan_theta', 'tan_varphi', 'tan_inc']
        part_list=[]
        for key in keys_topar:
            kwargs_right=kwargs.copy()
            kwargs_left=kwargs.copy()
            if not kwargs[key]==0:
                kwargs_right[key]*=(1+delta)
                kwargs_left[key]*=(1-delta)
                hres_right=self.response(kwargs_right)
                hres_left =self.response(kwargs_left)
                part=(hres_right-hres_left)/(2*kwargs[key]*delta)
            else:
                kwargs_right[key]+=delta
                kwargs_left[key]-=delta
                hres_right=self.response(kwargs_right)
                hres_left =self.response(kwargs_left)
                part=(hres_right-hres_left)/(2*delta)
#             kwargs_right[key]*=(1+delta)
#             kwargs_left[key]*=(1-delta)
#             hres_right=self.response(kwargs_right)
#             hres_left =self.response(kwargs_left)
#             part=(hres_right-hres_left)/(2*kwargs[key]*delta)

            #part=max((hres_right-hres_left)/(2*kwargs[key]), 1e-30) # to prevent singular matrix
            #part=np.where(np.abs(hres_right-hres_left)>1e-50,(hres_right-hres_left)/(2*kwargs[key]),1e-50/(2*kwargs[key]))
            # part is np.array of complex number
            part_list.append(part)
        part_nparray=np.array(part_list) # [7*dim(f)]
        mat_part=np.einsum('i..., j...-> ij...', np.conj(part_nparray), part_nparray) # [7*7*dim(f)]
        #self.mat_part=mat_part
        return mat_part

    def fisher_max(self, mat_part):
        """

        """
        len_f=mat_part.shape[2] # the length of frequency dimension
        frequencies = np.arange(len_f)
        #if mat_part==None:
        #    mat_part=self.mat_part
        freq, noise_power=self.det.noise_curve()
        noise_power_corresponding=np.interp(frequencies, freq, noise_power)
        FIM_integrand=mat_part/noise_power_corresponding
        FIM = 4. * np.sum(FIM_integrand, axis=2)
        #self.FIM=FIM
        return np.real(FIM)

    def Cov(self, FIM=None):
        #if FIM==None:
        #    FIM=self.FIM
        a=np.linalg.inv(FIM)
        return a

    def attach_error_single(self, GW_source, know_loc=1):
        """
        GW_source is a dict of single source parameters
        """
        # give him a phi0~


        GW_source['phi0']=np.pi
        # give him tan angles
        GW_source['tan_inc']=np.tan(GW_source['inc']-np.pi*0.5)
        GW_source['tan_psi']=np.tan(GW_source['psi']-np.pi*0.5)
        GW_source['tan_theta']=np.tan(GW_source['theta']-np.pi*0.5)
        GW_source['tan_varphi']=np.tan(GW_source['varphi']*0.5-np.pi*0.5)
        GW_source['tan_phi0']=np.tan(GW_source['phi0']*0.5-np.pi*0.5)

        # give him ln D
        #GW_source['logD']=np.log10(GW_source['D'])

        if know_loc==1:
            mat_part=self.partial_know_loc(GW_source)
            error_dim=['m1', 'm2', 'χ', 'D', 'tan_psi', 'tan_phi0', 'tan_inc']
        elif know_loc==0:
            mat_part=self.partial(GW_source)
            error_dim=['m1', 'm2', 'χ', 'D', 'tan_psi', 'tan_phi0', 'tan_theta', 'tan_varphi', 'tan_inc']
        elif know_loc==2:
            mat_part=self.partial_know_toomuch(GW_source)
            error_dim=['m1', 'm2', 'χ', 'D', 'tan_inc']
        FIM=self.fisher_max(mat_part=mat_part)
        covariance=self.Cov(FIM=FIM)
        #key_list=GW_source.keys()
        GW_source_we=GW_source.copy()
        for i in range(len(error_dim)):
            new_key='d'+error_dim[i]
            GW_source_we[new_key]=np.sqrt(np.abs(covariance[i,i]))

        return GW_source_we

    def attach_error_dataframe(self, GW_cat, know_loc=1):
        """
        GW_cat is pd.dataframe
        """
        event_list=GW_cat.to_dict('records')
        event_list_we=[]
        for GW_source in event_list:
            GW_source_we=self.attach_error_single(GW_source, know_loc=know_loc)
            event_list_we.append(GW_source_we)
        GW_cat_we=pd.DataFrame(event_list_we)
        return GW_cat_we
