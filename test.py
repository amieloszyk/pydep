import pydep.material as mat
reload(mat)
test = mat.Material()
test.add_iso('U238')
test.add_iso('Np239')
test.add_iso('Pu239')
test.add_iso('Pu240')
dens = 10.97*100.**3/(238.+32.)*6.022e23
test.set_dens('U238',dens=dens*0.99)
test.set_dens('Pu239',dens=dens*0.01)
test.set_ng_path('U238','Np239')
test.set_ng_path('Pu239','Pu240')
test.set_decay('Np239',t_half=2.3565,daught_name=['Pu239'],half_unit='d')
test.dec_const
test.set_decay('Np239',t_half=2.3565,daught_name=['Pu239'],half_unit='day')
test.dec_const
test.ng_branch
test.ng_ind
test.n2n_ind
test.fiss_ind
test.daught_ind
test.set_ng_path('Pu239','Pu240')
test.N_vect
sig_c_U238 = 5./1.0e24/100.**2
sig_c_Pu239 = 1./1.0e24/100.**2
sig_f_Pu239 = 3./1.0e24/100.**2
test.N_name
time = 3600.0*24.0
dt = 3600.0*24.0
time = 0.0
U238 = [100.]
Np239 = [0.]
Pu239 = [1.]
Pu240 = [0.]
time = [0.0]
while time[-1] < 100.*3600.*24.:
        time.append(time[-1]+dt)
        test.set_ng_XS('U238',sig_c_U238)
        test.set_ng_XS('Pu239',sig_c_Pu239)
        test.set_fiss_XS('Pu239',sig_f_Pu239)
        test.deplete_step(dt)

