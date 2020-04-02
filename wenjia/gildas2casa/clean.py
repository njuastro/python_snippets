# run in casa, if you have a uvtfile = 'a.uvt':
# CASA<1>: execfile('clean.py')
# CASA<2>: run('a.uvt')


from astropy.io import fits

def run(uvtfile):

    uvfitsfile = uvtfile[:-4]+".uvfits"
    os.system("/opt/local/bin/greg @ from_gildas_to_uvfits.greg "+uvtfile+" "+uvfitsfile)  # greg path to be changed

    hdul = fits.open(uvfitsfile, mode='update')
    hdul[0].header['SPECSYS'] = hdul[0].header['SSYSSRC']
    hdul[0].header['CRVAL4'] = hdul[0].header['RESTFREQ'] * (1.0 -hdul[0].header['ZSOURCE']/2.99792458E+08)
    hdul.close()
    
    uvfits = uvfitsfile  
    vis    = str(uvfitsfile)[:-7]+".ms"

    os.system("rm -rf "+vis)
    importuvfits(fitsfile=uvfits,vis=vis)
    
    listobs(vis,listfile=str(uvfitsfile)+'listobs.list',overwrite=True)
    
    os.system("rm -rf "+str(uvfitsfile)[:-7]+".im*")
    imagename =str(uvfitsfile)[:-7]+".im"
    tclean(vis          = vis,
            imagename  = imagename,
            imsize     = 300, 
            cell       = '0.1arcsec',
            niter      = 500,
            specmode   = 'cube',
            restfreq   = '229.96GHz'
            )  # parameteres should be changed accordingly

    exportfits(imagename=imagename+".image",fitsimage=imagename+".fits" ,overwrite=True)
