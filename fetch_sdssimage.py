#!/usr/bin/env python

"""It is a python implementation about the SDSS online tools: Finding 
Chart: https://github.com/njuastro/python_snippets.git

Basically, it can get the sdss image online after you provide the coordinates.

Requirements:
    python >3.5
    numpy 
    matplotlib >2.0
    requests
    pillow
    astropy >1.0

Usage:
1. As a function:

    # in python
    from fetch_sdssimage import image_fetch
    image_fetch(ra=179.689293428354, dec=-0.454379056007667)

2. As a command-line-tool

    # in terminal
    $ python fetch_sdssimage.py -h
    $ python fetch_sdssimage.py --ra 179.689293428354 --dec -0.454379056007667 
    
    # make it executable
    $ chmod +x fetch_sdssimage.py
    $ ./fetch_sdssimage.py --ra 179.689293428354 --dec -0.454379056007667 


Author: Jianhang Chen
Email: cjhastro@gmail
History:
    2020.03.26: first release, version=0.0.1

"""

import argparse
import io
import numpy as np
from matplotlib import pyplot as plt
import PIL
import requests

# keep track of your version
version = '0.0.1'


def image_fetch(ra=None, dec=None, ax=None, showImage=True, mini=True, scale=0.1,
                width=640, height=640, band='R', opt='G', lw=1, fs=8, 
                mag_range=(0, 21), showName=False, target_name='Undefined'):
    """Fetch the sdss RGB image

    Parameters
    ----------
    ra : float
        the right ascension of the target
    dec : float
        the declination of the target
    ax : object
        pyplot axis object
    scale : float 
        angular size per pixel
    width : float
    height : float
        size of the image (in pixel)
    band : str
        the photometric band to be download (deprecated)
    opt : str
    mag_range : list
        online options see http://skyserver.sdss.org/dr16/en/tools/chart/chartinfo.aspx
    lw : float
        line width
    fs : float
        font size
    target_name : str
        the name of your target
    showName : bool
        put the name of target into the image
    showImage : bool
        show the image interactively
    """
    # define the server url
    base_url = 'http://skyserver.sdss.org/dr14/SkyServerWS/ImgCutout/getjpeg?ra={ra}&dec={dec}&scale={scale}&width={width}&height={height}&opt={opt}&query={band} {mag_range}'
    url = base_url.format(ra=ra, dec=dec, scale=scale,
                          width=width, height=height, band=band, opt=opt,
                          mag_range=mag_range)
    r = requests.get(url)
    
    # check return status of the server
    if r.status_code != 200:
        raise ValueError("request error! url:{}".format(url))
    # read the online image
    im = PIL.Image.open(io.BytesIO(r.content))
    ax1, ax2 = im.size

    # check if provide the axis, if not, make a new one
    if ax == None:
        fig = plt.figure()
        ax = fig.add_subplot(111)
    ax.imshow(im)

    # remove the tick labels
    if mini:
        ax.set_xticklabels([])
        ax.set_yticklabels([])

    # add the name in the image, the name should be provided by name='your name'
    if showName:
        ax.text(width*0.5, height*0.1, target_name, color='white', fontsize=fs, ha='center', va='center')
       
    if showImage:
        if ax == None:
            return fig
        plt.show()
    else:
        fig.savefig(target_name + '.png', bbox_inches='tight')


if __name__ == '__main__':
    # make script work in the cmd
    parser = argparse.ArgumentParser(description="generate mask file for BBarolo")
    parser.add_argument('--ra', default=None, type=float)
    parser.add_argument('--dec', default=None, type=float)
    parser.add_argument('--width', default=640, type=float)
    parser.add_argument('--height', default=640, type=float)
    parser.add_argument('--scale', default=0.1, type=float)
    parser.add_argument('--version', action='version', version=version)

    args = parser.parse_args()

    image_fetch(ra=args.ra, dec=args.dec, scale=args.scale, width=args.width, 
                height=args.height)
