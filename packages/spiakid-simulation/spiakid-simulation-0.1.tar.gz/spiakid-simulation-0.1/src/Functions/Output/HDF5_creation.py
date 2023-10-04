import h5py
import numpy as np

def h5_save(Link,sim):
    r""" Save the simulation in an HDF5 format file

    Paramters:
    ----------

    Link: string
        File path of the place to save the simulation
    
    sim: obj
        The simulation

    Output:
    -------

    None
    
    
    """
    f = h5py.File(Link,'w')
    grp = f.create_group('data')
    for k, v in sim.data.items():
        if type(sim.data[k]) == dict:
                    sub = grp.create_group(k)
                    for k1,v1 in sim.data[k].items():
                        if type(sim.data[k][k1]) == dict:
                            sub2 = sub.create_group(k1)
                            for k2,v2 in sim.data[k][k1].items():
                                sub2[k2] = v2
                        else:
                            sub[k1] = v1
        else:
            grp[k] = v
    if sim.data['3-Phase']['Phase'] == True:
        if (sim.data['3-Phase']['Noise']['type'] == 'Gaussian')|(sim.data['3-Phase']['Noise']['type'] == 'Poisson'):
            grp2 = f.create_group('Phase')
        grp3 = f.create_group('Phase_exp')
        dim = np.shape(sim.phase_exp)
        for i in range(dim[0]):
            for j in range(dim[1]):
                grp3['%d'%(i)+'%d'%(j)] = sim.phase_exp[i,j]
                if (sim.data['3-Phase']['Noise']['type'] == 'Gaussian')|(sim.data['3-Phase']['Noise']['type'] == 'Poisson'):
                    grp2['%d'%(i)+'%d'%(j)] = sim.phase[i,j]
        grp4 = f.create_group('Photon')
        dim = np.shape(sim.Fits_photon)
        for i in range(dim[0]):
            for j in range(dim[1]):
                grp4['%d'%(i)+'%d'%(j)] = sim.Fits_photon[i,j]
    f.close()
