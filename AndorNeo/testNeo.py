#!/usr/bin/python

###############
# testNeo.py
#
# Copyright David Baddeley, 2012
# d.baddeley@auckland.ac.nz
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
################

from __future__ import absolute_import
import time
from copy import copy
import numpy as np
import logging
logging.basicConfig(format='%(asctime)s.%(msecs)03d %(filename)s/%(funcName)s:%(lineno)d %(message)s', datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.WARNING)

def basicNeoTest(nframe,nbuffer):
    logging.info('Importing Camera')
    import AndorNeo
    #%%
    logging.info('Initialising Camera')
    cam = AndorNeo.AndorNeo(0,nbuffer)
    cam.Init()

    cam.SetIntegTime(1) #exposure milliseconds
    #cam.PixelReadoutRate.setIndex(2)
    #%%
    logging.info('Starting Exposure')
    cam.StartExposure()

    # this is one single frame, no more
    rbuf,cbuf = cam.GetPicWidth(),cam.GetPicHeight()
    buf = np.empty((rbuf,cbuf ), np.uint16)
    
    #output image array
    imgs = []#np.empty((nbuffer,cbuf,rbuf),np.uint16)

    logging.info('Starting Extraction loop')
    time.sleep(1) #will get blank images without at least 62.5ms delay! (60.0ms doesn't work)
    for i in range(nframe):
        while cam.ExpReady():
            cam.ExtractColor(buf, 1)
            # WARNING: copy(buf) is absolutely necessary or all images will be the same!
            imgs.append(copy(buf).reshape((cbuf,rbuf),order="C"))
            
    cam.Shutdown()
    time.sleep(.05)
    AndorNeo.camReg.unregCamera()  

    return imgs
    
if __name__ == '__main__':
    import h5py
    from matplotlib.pyplot import figure,draw,pause
    
    imgs = basicNeoTest(3,1)
    print('{} images returned'.format(len(imgs)))
    
    with h5py.File('blah.h5','w',libver='latest') as f:
        f['/imgs'] = imgs
    
    if 0:
        fg = figure()
        ax = fg.gca()
        hi=ax.imshow(imgs[0],cmap='gray')
        for i,I in enumerate(imgs):
            hi.set_data(I)
            #fg.colorbar(hi)
            ax.set_title(i)
            draw()
            pause(0.01)
        
    if False:    
        for I in imgs:
            cv2.imshow('frame',I)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break