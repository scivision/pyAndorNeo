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
import numpy as np
import logging
logging.basicConfig(format='%(asctime)s.%(msecs)03d %(filename)s/%(funcName)s:%(lineno)d %(message)s', datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

def basicNeoTest(nframe):
    logging.info('Importing Camera')
    import AndorNeo
    #%%
    logging.info('Initialising Camera')
    cam = AndorNeo.AndorNeo(0)
    cam.Init()

    cam.SetIntegTime(1) #exposure milliseconds
    #cam.PixelReadoutRate.setIndex(2)
    #%%
    logging.info('Starting Exposure')
    cam.StartExposure()

    # this is one single frame, no more
    buf = np.empty((cam.GetPicWidth(), cam.GetPicHeight()), np.uint16)

    logging.info('Starting Extraction loop')
    for i in range(nframe):
        while cam.ExpReady():
            cam.ExtractColor(buf, 1)
        
        time.sleep(.001)
            
    time.sleep(1)

    cam.Shutdown()
    time.sleep(1)
    AndorNeo.camReg.unregCamera()  

    return buf
    
if __name__ == '__main__':
    buf = basicNeoTest(10)