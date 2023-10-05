import numpy as np
import numpy.random as rand
import matplotlib.pyplot as plt
from pathlib import Path
from scipy import signal
from scipy.optimize import least_squares
from astropy.io import fits
from astropy.wcs import WCS

# Return 2D-gaussian on a kerlen size radius
def gkern(kernlen=21,std=1):
    """Returns a 2D Gaussian kernel array."""
    gkern1d = signal.windows.gaussian(kernlen, std=std).reshape(kernlen, 1)
    gkern2d = np.outer(gkern1d, gkern1d)
    return gkern2d

def fit_aff(dist, size):
        def model(x,u):
            return(x[0]*u + x[1])     
        def fun(x,u,y):
            return(model(x,u) - y)
        def Jac(x,u,y):
            J = np.empty((u.size,x.size))
            J[:,0] = u
            J[:,1] = 1
            return(J)
        t = np.array(dist)
        dat = np.array(size)
        x0 = [1,1]
        res = least_squares(fun, x0, jac=Jac, args=(t,dat)) 
        return res.x[0],res.x[1]

def Dist2Size(dist):
    #Init
    Calib_dist = [1,10,10,1000]
    Calib_size = [10,7,5,2]
    func = fit_aff(Calib_dist,Calib_size)
    size = func[0] * dist + func[1]

    return(int(size))

def Image_Sim(Image_size, object_number,save = False):
    # Image Creation

    Image = np.zeros([Image_size,Image_size])

    # importing spectrums
    files = Path('/spiakid/SPIAKID_LIB').glob('F*')
    Spectrum_path = []
    for i in files:
        Spectrum_path.append(i)

    Object_dict = {}
    size_list = []
    # Object creation (position + spectrum path)
    for i in range(object_number):
        pos_x = rand.randint(np.shape(Image)[0])
        pos_y = rand.randint(np.shape(Image)[1])
        Object_dict[pos_x,pos_y] = {}
        Object_dict[pos_x,pos_y]['Position'] = [pos_x,pos_y]
        Object_dict[pos_x,pos_y]['Spectrum'] = np.loadtxt(Spectrum_path[rand.randint(len(Spectrum_path))])
        data_init = np.loadtxt(Spectrum_path[rand.randint(len(Spectrum_path))])
        Object_dict[pos_x,pos_y]['Distance'] = rand.randint(100,500) # Distance Parsec
        Object_dict[pos_x,pos_y]['Size'] = 5
        size_list.append(Object_dict[pos_x,pos_y]['Size'])
        Image[pos_x,pos_y] = 1


    # Creation of an intermediate Image 
    ext = int((max(size_list)+1)/2)
    Image_inter = np.zeros([Image_size + 2*ext,Image_size + 2*ext])
    spec_image = []

    # # Creation of 2D Gaussian on the intermedite image
    for i in Object_dict:
        pos_x, pos_y = Object_dict[i]['Position']
        Image_inter[pos_x + ext - int((Object_dict[i]['Size'])/2):pos_x + ext + int((Object_dict[i]['Size']+1)/2),pos_y + ext - int((Object_dict[i]['Size'])/2):pos_y + ext + int((Object_dict[i]['Size']+1)/2)] += gkern(Object_dict[i]['Size']) * 1 / Object_dict[i]['Distance']**2
        for k in range (pos_x + ext - int((Object_dict[i]['Size'])/2),pos_x + ext + int((Object_dict[i]['Size']+1)/2)):
            for l in range (pos_y + ext - int((Object_dict[i]['Size'])/2),pos_y + ext + int((Object_dict[i]['Size']+1)/2)):
                if k - ext >= 0 and l - ext >= 0 and l - ext < Image_size and k - ext < Image_size:
                    spec_image.append([k-ext,l-ext,Object_dict[i]['Spectrum'][:,1] * 1 / Object_dict[i]['Distance']**2 * Image_inter[k,l]] )
    # # Cutting the intermediate image  
    Image2 = Image_inter[ext:Image_size+ext,ext:Image_size+ext]
    Data_cube = np.zeros([np.shape(Image2)[0],np.shape(Image2)[1],1+len(data_init[:,0])])
    Data_cube[:,:,0] = Image2
    Data_cube[:,:,1:] = np.zeros(len(data_init[:,0]))
    for i in range(len(spec_image)):
        Data_cube[spec_image[i][0],spec_image[i][1],1:] += spec_image[i][2]
    
    if save == True:
        hdr = fits.Header()
        hdr['CTYPE1'] = 'Spectrum'
        hdr['CTYPE2'] = 'Pixel_y'
        hdr['CTYPE3'] = 'Pixel_x'
        hdr['CUNIT1'] = 'pix'
        hdr['CUNIT2'] = 'pix'
        hdr['CUNIT3'] = 'W/m**2/nm'
        primary_hdu = fits.PrimaryHDU(Data_cube,header=hdr)
        wv_hdu = fits.ImageHDU(data_init[:,0])
        hdul = fits.HDUList([primary_hdu,wv_hdu])
        hdul.writeto('/spiakid/data/Simulation_Image/Image.fits',overwrite=True)
    return(Data_cube,data_init[:,0])
