import numpy as np

class Material(object):

    def __init__(self,mat_id=None,name=''):
        '''Initialize the class.'''

        self.N_name = []
        self.N_vect = []
        self.ng_name = []
        self.ng_ind = []
        self.n2n_name = []
        self.n2n_ind = []
        self.dec_const = []
        self.daught_name = []
        self.daught_ind = []
        self.branch_rat = []

    def add_iso(self,name,dens=0.0,den_unit='1/m3'):
        '''Add an isotope to track.'''

        self.N_name.append(name)
        if '/cm3' in den_unit:
            dens *= 100.**3
        elif 'brn' in den_unit:
            dens *= 1.0e24
            if 'cm' in den_unit:
                dens *= 100.0
        self.N_vect.append(dens)
        self.ng_name.append('')
        self.ng_ind.append(-1)
        self.n2n_name.append('')
        self.n2n_ind.append(-1)
        self.dec_const.append(0.0)
        self.daught_name.append('')
        self.daught_ind.append(-1)
        self.branch_rat.append([1.0])

    def get_ind(self,name,attr):
        '''Get the index associated with the name.'''

        temp = getattr(self,attr)
        if name in temp:
            ind = temp.index(name)
        else:
            ind = -1

        return ind

    def set_dens(self,name=None,ind=None,dens=0.0,den_unit='1/m3'):
        '''Reset the number density of a value.'''

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

    def set_nrx(self,name,rx_name,rx_type):
        '''Set the (n,rx) daughter'''

        ind_from = self.get_ind(name,'N_name')
        ind_to = self.get_ind(rx_name,'N_name')
        getattr(self,rx_type+'_name')[ind_from] = rx_name
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
        self.branch_rat[parent_ind] = branch
