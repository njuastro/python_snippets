from astropy.io import ascii as at
import matplotlib.pyplot as plt
import astropy.units as u


imagename = 'merged.3kms.im.image'  # to be changed

myoutput = imval(imagename = imagename, region='IZw18-CO21.crtf')  # region to be changed

flux = np.nanmean(myoutput['data'],axis=(0,1)) # Jy/beam mean flux 
freq = myoutput['coords'][0,0,:,3]/1e9  #GHz  
Mask = myoutput['mask'][:,:,0]
MyAperPixels   =  np.sum(np.ones(Mask.shape)[Mask])


#================= convert from jy/beam to jy ===================


# ------read header file --------
myhead    =  imhead(imagename,mode='list')
channels  =  myhead['perplanebeams']['nChannels'] #  #channels  =  SpecExtrCube.shape[2] The same 



# -initialise bmaj and bmin array for each channel 
bmaj      =  np.arange(channels)*1.0 
bmin      =  np.arange(channels)*1.0
bpa       =  np.arange(channels)*1.0


for i in range(0, channels):
#   print(i)
    bmaj[i] = myhead['perplanebeams']['*'+str(i)]['major']['value']
    bmin[i] = myhead['perplanebeams']['*'+str(i)]['minor']['value']
    bpa[i]  = myhead['perplanebeams']['*'+str(i)]['positionangle']['value']



# --- Read and assign beam values to the arrays 
#     Obtain beamsize/shape of each channel varies.

#get pixel size in arcsec  
pixelsize    = np.abs((myhead['cdelt1']* u.rad).to(u.arcsec).value)
# beam area calculated from a 2-D Gaussian  in arcsec^2  
MyBeamArea   = np.pi*  bmaj * bmin / ( 4 * np.log(2) ) 
# How many pixels in one beam 
MyBeamPixels = MyBeamArea / (pixelsize**2 )
FluxDensity  = flux/ MyBeamPixels * MyAperPixels  *1e3 # mJy 

#======================= plot the spectrum =====================
nu   =  float(myhead['crval4'])/1e9       # reference frequence in GHz 
c    = 3e5  #speed of light km/s
velo = (nu-freq)/nu*c


fig, ax = plt.subplots(figsize = (15,5))
plt.step(velo,FluxDensity,where='mid')
plt.xlabel('velocity (km/s)',fontsize=18)
plt.ylabel(r'f$_\nu$(mJy)',fontsize=18)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.title(imagename,fontsize = 18)
plt.xlim(-120,120)
plt.grid()
plt.show()
plt.savefig(imagename+'.pdf')


#at.write([FluxDensity,freq],'spec-crtf.txt',overwrite=True)
