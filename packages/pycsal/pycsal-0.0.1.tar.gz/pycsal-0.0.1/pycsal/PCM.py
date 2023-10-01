import numpy as np
import asaplib
from asaplib.data import ASAPXYZ
from asaplib.reducedim import Dimension_Reducers


def asap_pcm(inp, n_process=1, n_components=2, navg=5):
    #calculate the PCM of data
    asapxyz = ASAPXYZ(inp, periodic=True) # periodic=False otherwise


# specify the parameters
    soap_spec = {'soap1': {'type': 'SOAP',
                       'cutoff': 4.0,
                       'n': 6,
                       'l': 6,
                       'atom_gaussian_width': 0.5,
                       'crossover': False,
                       'rbf': 'gto'
                      }
            }

    reducer_spec = {'reducer1': {
                          'reducer_type': 'average', # [average], [sum], [moment_average], [moment_sum]
                          'element_wise': False}
               }

    desc_spec = {'avgsoap': {
                  'atomic_descriptor': soap_spec,
                  'reducer_function': reducer_spec}
            }


    # compute atomic descriptors only
    asapxyz.compute_atomic_descriptors(desc_spec_dict=soap_spec,
                                    sbs=[],
                                    tag='xxx-atomic',
                                    n_process=1)


    # compute descriptors for the whole structures
    asapxyz.compute_global_descriptors(desc_spec_dict=desc_spec,
                                    sbs=[],
                                    keep_atomic=False, # set to True to keep the atomic descriptors
                                    tag='xxx',
                                    n_process=n_process)


    reduce_dict = {}
    reduce_dict['kpca'] = {"type": 'SPARSE_KPCA',
                        'parameter':{"n_components": n_components,
                                     "n_sparse": -1, # no sparsification
                                "kernel": {"first_kernel": {"type": 'linear'}}}}


    dreducer = Dimension_Reducers(reduce_dict)

    dm = asapxyz.fetch_computed_descriptors(['avgsoap'])
    proj = dreducer.fit_transform(dm)
    Ndata = len(proj)
    dis = np.zeros( (Ndata, Ndata)  )
    for i in range(Ndata):
        for j in range(i, Ndata):
            dis[i, j] = np.linalg.norm(proj[i] - proj[j])
            dis[j, i] = dis[i, j]
#    print(dis)
    avgdis = np.zeros(Ndata)
    for i in range(Ndata):
        dis_i = sorted(list(dis[i, :]))
        avg = np.mean(dis_i[1:navg+1])
        avgdis[i] = avg
    np.savetxt('proj.txt', proj)
#    print (avgdis)
    return avgdis

#inp = 'pick1.xyz'
#asap_pcm(inp, n_process=1, n_components=2)

