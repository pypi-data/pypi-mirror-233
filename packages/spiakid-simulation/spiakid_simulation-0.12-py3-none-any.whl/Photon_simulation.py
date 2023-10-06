import numpy as np

import Functions.Output.HDF5_creation as hdf
import Functions.Yaml.Yaml_rw as yml
import Functions.Image.Photon_gen_image as Image_Gen
import Functions.Image.Black_Body_Filter as BB
import Functions.Noise.Noise_add as N
import Functions.Timeline.Timeline as Tl
import Functions.Phase.Phase_conversion as Ph
import Functions.Phase.Calib_read as Cr
import Functions.IQ.IQ_sim as IQ

class Photon_simulator():
    r"""" Launch the simulation by reading the yaml file and return all the computed information

    Parameter:
    ----------

    Yaml_path: string
        Path to the YAML input file

    Attributes:
    -----------

    Data: Dictionnary
            Contains all information that contains the yaml file correctly ordered

    Fits_photon: array
            How many photons per pixels

    Wavelength_ok, Radiance_ok, Wavelength_out, Radiance_out: array
            The wavelength and radiance of photons. Pass through the filter in _ok, blocked by the filter in _out

    Photon_Timeline: array
            Wavelength and arrival time of photon 

    Phase_conversion: array
            Phase corresponding to each photon through the time
        
    Phase_exp: array
            Phase followed by a decreasing exponential, representing the energy dissipation
        
    Phase: array
            Phase_exp with noise

    IQ_conversion: array
            IQ corresponding to each photon through the time

    IQ_exp: array
            IQ followed by a decreasing exponential, representing the energy dissipation

    IQ: array
            IQ with noise
    
    """

    def __init__(self, yaml_path):
        self.photon = []
        self.simulated_photon = []
        
        # Reading all data in the yaml
        self.data = yml.read_yaml(yaml_path)

        # Definition of dictionnaries
        photon_gen = self.data['1-Photon_Generation']
        # print(type(photon_gen))
        detector_dim = [photon_gen['Detector']['row'],photon_gen['Detector']['row']]
        Method = photon_gen['Method']['method']
        Filter = photon_gen['Method']['Filter']
        Noise = photon_gen['Noise']

        # Checking which method to use (Image and Black body for now)

        # Method Image with .fits 
        if  Method == 'Fits':
            #Taking Parameters
            Path = photon_gen['Method']['Path']
            center = photon_gen['Method']['Center']
            zoom = photon_gen['Method']['Zoom']
            #Generating photons
            self.Fits_photon = Image_Gen.Photon_gen( FitsPath= Path,detector_dim=detector_dim,center = center, zoom = zoom)
            print('Photon Generated')
            #Adding Noise on the photon number
            if Noise['type'] == 'Gaussian':
                scale = Noise['scale']
                loc = Noise['loc']
                self.Fits_photon = N.Gaussian_noise(self.Fits_photon, location=loc, scale=scale)
            elif Noise['type'] == 'Poisson':
                self.Fits_photon = N.Poisson_noise(self.Fits_photon)
            else:
                pass
            # Each photon source is a black body
            if Filter == 'Black Body':
                # Taking information required 
                Temperature = photon_gen['Method']['Temperature']
                print('Photon Filter')
                # assign wavelength to each photon on each pixel
                self.Wavelength_ok,self.Radiance_ok,self.Wavelength_out,self.Radiance_out = BB.BB_filter(Temperature= Temperature,FitsPhoton = self.Fits_photon)
        elif Method == 'spectrum':
            print('Not done yet')

        # Creation of a Timeline
        Exposure_time = self.data['2-Timeline']['Time']
        Point_nb = self.data['2-Timeline']['Point_nb']
        self.Photon_Timeline = Tl.sorting(Exposure_time,self.Wavelength_ok,Point_nb)

        # Do we want to simulate the phase or IQ ?
        try:self.data['3-Phase']
        except:
            # We don't want to simulate the phase
            try: self.data['3-IQ']
            # We don't want to simulate nor the phase neither IQ
            except: pass
            # We want to simulate IQ
            else: self.IQ_Compute(obj = '3-IQ')
        # We want to simulate  IQ
        else: self.Phase_compute(detector_dim=detector_dim,obj = '3-Phase')

        if type(self.data['4-Output']['Link']) == str:
            hdf.h5_save(self.data['4-Output']['Link'],self)




    def Phase_compute(self, detector_dim,obj):
        if self.data[obj]['Phase'] == True:
            # Reading convertion coeff
            try: self.data[obj]['Conv_wv'] and self.data[obj]['Conv_phase']
            except: 
                try: self.data[obj]['Calib_File']
                except: 
                    Cr.write_csv('Calib.csv',dim = detector_dim, sep = '/')
                    pix,conv_wv,conv_phase = Cr.read_csv('Calib.csv')
                else: pix,conv_wv,conv_phase = Cr.read_csv(self.data[obj]['Calib_File'])

            else:
                pix = []
                conv_wv = []
                conv_phase = []
                for i in range(detector_dim[0]):
                    for j in range(detector_dim[1]):
                        pix.append(str(i)+str(j))
                        conv_wv.append(self.data[obj]['Conv_wv'])
                        conv_phase.append(self.data[obj]['Conv_phase'])
            
            #Conversion photon to phase
            self.Phase_conversion = Ph.phase_conv(self.Photon_Timeline,pix = pix,conv_wv=conv_wv, conv_phase=conv_phase)
            Decay = self.data[obj]['Decay']
            #Adding exponential
            self.phase_exp = Ph.exp_adding(self.Phase_conversion, Decay)

            # Adding Noise
            if self.data[obj]['Noise']['type'] == 'Gaussian':
                phase = np.copy(self.phase_exp)
                loc = self.data[obj]['Noise']['loc']
                scale = self.data[obj]['Noise']['scale']
                self.phase =  N.Gaussian_noise(phase,location=loc,scale=scale)
            elif self.data[obj]['Noise']['type'] == 'Poisson':
                phase = np.copy(self.phase_exp)
                self.phase = N.Poisson_noise(phase)
            else:
                pass
        else:
            pass
    
    def IQ_Compute(self,obj):
        if self.data[obj]['IQ'] == True:
            try: self.data[obj]['Calib_file_csv']
            except:
                self.IQ_conversion = IQ.photon2IQ_th(self.Photon_Timeline)
            else:
                self.IQ_conversion = IQ.photon2IQ_csv(self.Photon_Timeline, Path = self.data[obj]['Calib_file_csv'])
            Decay = self.data[obj]['Decay']
            self.IQ_exp = IQ.exp_adding(self.IQ_conversion, Decay)
            # Adding Noise
            if self.data[obj]['Noise']['type'] == 'Gaussian':
                    sig = np.copy(self.IQ_exp)
                    loc = self.data[obj]['Noise']['loc']
                    scale = self.data[obj]['Noise']['scale']
                    self.IQ =  [N.Gaussian_noise(sig[0],location=loc,scale=scale),N.Gaussian_noise(sig[1],location=loc,scale=scale)]
            elif self.data[obj]['Noise']['type'] == 'Poisson':
                    sig = np.copy(self.IQ_exp)
                    self.IQ = [N.Poisson_noise(sig[0]),N.Poisson_noise(sig[1])]
            else:
                    pass
        else:
            pass
            



