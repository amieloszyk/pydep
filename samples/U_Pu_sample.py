import pydep.material as mat

upu_chain = mat.Material()

iso_list = ['U234','U235','U236','U237','U238','Np237','Np238','Np239',\
    'Pu238','Pu239','Pu240','Pu241','Pu242']

for name in iso_list:
    upu_chain.add_iso(name)

upu_chain.set_ng_path('U234','U235')
upu_chain.set_ng_path('U235','U236')
upu_chain.set_ng_path('U236','U237')
upu_chain.set_ng_path('U237','U238')
upu_chain.set_ng_path('U238','Np239')
upu_chain.set_ng_path('Np237','Np238')
upu_chain.set_ng_path('Np238','Np239')
upu_chain.set_ng_path('Np239','Pu240')
upu_chain.set_ng_path('Pu238','Pu239')
upu_chain.set_ng_path('Pu239','Pu240')
upu_chain.set_ng_path('Pu240','Pu241')
upu_chain.set_ng_path('Pu241','Pu242')
upu_chain.set_ng_path('Pu241','Pu242')
upu_chain.set_ng_path('Pu242','Am243')

upu_chain.set_n2n_path('U234','U232')
upu_chain.set_n2n_path('U235','U233')
upu_chain.set_n2n_path('U236','U234')
upu_chain.set_n2n_path('U237','U235')
upu_chain.set_n2n_path('U238','U236')
upu_chain.set_n2n_path('Np237','Np235')
upu_chain.set_n2n_path('Np238','Np236')
upu_chain.set_n2n_path('Np239','Np237')
upu_chain.set_n2n_path('Pu238','Pu236')
upu_chain.set_n2n_path('Pu239','Pu237')
upu_chain.set_n2n_path('Pu240','Pu238')
upu_chain.set_n2n_path('Pu241','Pu239')
upu_chain.set_n2n_path('Pu242','Pu240')

# The below values are not correct, just for demonstration
upu_chain.set_decay('U234',dec_const=0.0,daught_name=['Np234'])
upu_chain.set_decay('U235',dec_const=0.0,daught_name=['Np235'])
upu_chain.set_decay('U236',dec_const=0.0,daught_name=['Np236'])
upu_chain.set_decay('U237',dec_const=0.0,daught_name=['Np237'])
upu_chain.set_decay('U238',dec_const=0.0,daught_name=['Np238'])
upu_chain.set_decay('Np237',dec_const=0.0,daught_name=['Pu237'])
upu_chain.set_decay('Np238',dec_const=0.0,daught_name=['Pu238'])
upu_chain.set_decay('Np239',dec_const=0.0,daught_name=['Pu239'])
upu_chain.set_decay('Pu238',dec_const=0.0,daught_name=['Am238'])
upu_chain.set_decay('Pu239',dec_const=0.0,daught_name=['Am239'])
upu_chain.set_decay('Pu240',dec_const=0.0,daught_name=['Am240'])
upu_chain.set_decay('Pu241',dec_const=0.0,daught_name=['Am241'])
upu_chain.set_decay('Pu242',dec_const=0.0,daught_name=['Am242'])
