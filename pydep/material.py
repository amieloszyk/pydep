import numpy as np

class Material(object):

    def __init__(self,rx_type=['fiss','ng','n2n']):
        '''Initialize the class.'''

        self.N_name = []
        self.N_vect = []
        self.dec_const = []
        self.daught_name = []
        self.daught_ind = []
        self.dec_branch = []
        self.Q_fiss = []

        self.rx_type = rx_type

        for rx in rx_type:

            setattr(self,rx+'_name',[])
            setattr(self,rx+'_ind',[])
            setattr(self,rx+'_branch',[])
            setattr(self,rx+'_XS',[])
            setattr(self,rx+'_rate_norm',[])

    def add_iso(self,name,dens=0.0,den_unit='1/m3'):
        '''Add an isotope to track.'''

        self.N_name.append(name)
        if '/cm3' in den_unit:
            dens *= 100.**3
        elif 'brn' in den_unit:
            dens *= 1.0e28
            if 'cm' in den_unit:
                dens *= 100.0
        self.N_vect.append(dens)
        self.dec_const.append(0.0)
        self.daught_name.append([''])
        self.daught_ind.append([-1])
        self.dec_branch.append([1.0])
        self.Q_fiss.append(0.0)

        for rx in self.rx_type:
            getattr(self,rx+'_name').append([''])
            getattr(self,rx+'_ind').append([-1])
            getattr(self,rx+'_branch').append([1.0])
            getattr(self,rx+'_XS').append(0.0)
            getattr(self,rx+'_rate_norm').append(0.0)

    def get_ind(self,name,attr):
        '''Get the index associated with the name.'''

        temp = getattr(self,attr)
        if name in temp:
            ind = temp.index(name)
        else:
            ind = -1

        return ind

    def set_dens(self,name=None,ind=None,dens=0.0,den_unit='1/m3'):
        '''Reset the number density of a value. (stored in 1/m3)'''

        if not ind:
            ind = self.get_ind(name,'N_name')
            if ind == -1:
                return None

        if '/cm3' in den_unit:
            dens *= 100.**3
        elif 'brn' in den_unit:
            dens *= 1.0e24
            if 'cm' in den_unit:
                dens *= 100.0
        self.N_vect[ind] = dens

    def set_Q_fiss(self,name,val):
        '''Set the fission Q value (in MeV)'''

        ind = self.get_ind(name,'N_name')

        self.Q_fiss[ind] = val

    def get_Q_fiss(self,name):
        '''Get the fission Q value (in MeV)'''

        ind = self.get_ind(name,'N_name')

        return self.Q_fiss[ind]

    def get_dens(self,name,unit='1/m3'):
        '''Get the density'''

        ind = self.get_ind(name,'N_name')

        dens = self.N_vect[ind]

        # Unit conversion
        if '/cm3' in unit:
            dens /= 100.**3
        elif 'brn' in unit:
            dens /= 1.0e24
            if 'cm' in unit:
                dens /= 100.0
        
        return dens

    def set_nrx(self,name,rx_name,rx_type):
        '''Set the (n,rx) daughter'''

        ind_from = self.get_ind(name,'N_name')
        ind_to = [self.get_ind(rx_name,'N_name')]
        getattr(self,rx_type+'_name')[ind_from] = [rx_name]
        getattr(self,rx_type+'_ind')[ind_from] = ind_to

    def set_ng_path(self,name,ng_name):
        '''Set (n,gamma) daughter path.'''
        
        self.set_nrx(name,ng_name,'ng')

    def set_n2n_path(self,name,n2n_name):
        '''Set (n,gamma) daughter path.'''
        
        self.set_nrx(name,n2n_name,'n2n')

    def set_decay(self,parent_name,dec_const=0.0,t_half=None,branch=[1.0],
        daught_name=[''],daught_ind=None,half_unit='sec'):
        '''Set the decay info for an isotope of interest.'''

        if t_half:
            
            if half_unit == 'hr':
                t_half *= 3600.0
            elif half_unit == 'day':
                t_half *= 3600.0*24.0
            elif half_unit == 'wk':
                t_half *= 3600.0*24.0*7.0
            elif half_unit == 'mon':
                t_half *= 3600.0*24.0*30.0
            elif half_unit == 'yr':
                t_half *= 3600.0*24.0*365.0

            dec_const = np.log(2.0)/t_half

        if not daught_ind:
            
            daught_ind = []

            for name in daught_name:
                
                daught_ind.append(self.get_ind(name,'N_name'))

        else:

            daught_name = []
            
            for ind in daught_ind:

                if ind != -1 and ind < len(self.N_name):

                    daught_name.append(self.N_name[ind])

                else:

                    daught_name.append('')

        parent_ind = self.get_ind(parent_name,'N_name')

        self.dec_const[parent_ind] = dec_const
        self.daught_name[parent_ind] = daught_name
        self.daught_ind[parent_ind] = daught_ind
        self.dec_branch[parent_ind] = branch

    def set_XS(self,name,val,rx_type):
        '''Set cross sections (stored in barns)'''

        ind = self.get_ind(name,'N_name')

        getattr(self,rx_type+'_XS')[ind] = val

    def get_XS(self,name,rx_type):
        '''Get cross sections (stored in barns)'''

        ind = self.get_ind(name,'N_name')

        return getattr(self,rx_type+'_XS')[ind]

    def set_rx_rate_norm(self,name,val,rx_type,units='1/sec'):
        '''Generically set the density normalized reaction rate.'''

        ind = self.get_ind(name,'N_name')
        
        getattr(self,rx_type+'_rate_norm')[ind] = val

    def set_ng_rate_norm(self,name,val,units='1/sec'):
        '''Set the density normalized (n,gamma) rate.'''

        self.set_rx_rate_norm(name,val,'ng',units=units)

    def set_n2n_rate_norm(self,name,val,units='1/sec'):
        '''Set the density normalized (n,2n) rate.'''

        self.set_rx_rate_norm(name,val,'n2n',units=units)

    def set_fiss_rate_norm(self,name,val,units='1/sec'):
        '''Set the density normalized fission rate.'''

        self.set_rx_rate_norm(name,val,'fiss',units=units)

    def build_A_mat(self,dt=None):
        '''Build the depletion A matrix.'''

        self.A = np.matrix([[0.0]*len(self.N_vect)]*len(self.N_vect))

        for j in xrange(len(self.N_vect)):

        #if dt: Bypass the decay

            # Reactions first
            for rx in self.rx_type:

                rate = getattr(self,rx+'_rate_norm')[j]

                self.A[j,j] -= rate

                for ind,rat in zip(getattr(self,rx+'_ind')[j],
                    getattr(self,rx+'_branch')[j]):

                    if ind != -1:

                        self.A[ind,j] += rate*rat

            # Now decay
            rate = self.dec_const[j]

            self.A[j,j] -= rate

            for ind,rat in zip(self.daught_ind[j],self.dec_branch[j]):

                self.A[ind,j] += rate*rat

    def Taylor_exp_mat(self,dt,M=15):
        '''Taylor expansion of exponential matrix.'''

        fact = 1.0
        E_mat = np.matrix([[0.0]*len(self.N_vect)]*len(self.N_vect))
        At = (self.A*dt)**0

        for m in xrange(M+1):

            if m != 0:
                fact *= float(m)
                At *= (self.A*dt)

            E_mat += 1.0/fact*At

        return E_mat

    def deplete_step(self,dt):
        '''Deplete one time step.'''

        self.build_A_mat()

        vect = np.transpose(np.matrix(self.N_vect))
        
        vect_new = np.transpose(self.Taylor_exp_mat(dt)*vect).tolist()

        self.N_vect = vect_new[0]

