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

def basicNeoTest():
    logging.info('Importing Camera ... ')
    import AndorNeo
    #%%
    logging.info('Initialising Camera ... ')
    cam = AndorNeo.AndorNeo(0)
    cam.Init()

    cam.SetIntegTime(100)
    #cam.PixelReadoutRate.setIndex(2)
    #%%
    logging.info('Starting Exposure ...')
    cam.StartExposure()

    buf = np.empty((cam.GetPicWidth(), cam.GetPicHeight()), 'uint16')

    print('Starting Extraction loop ...')
    for i in range(200):
        #print(i, end=' ')
        while cam.ExpReady():
            cam.ExtractColor(buf, 1)
            #print('e', end=' ')
        
        time.sleep(.2)
            
    time.sleep(20)

    cam.Shutdown()
    time.sleep(.5)
    AndorNeo.camReg.unregCamera()  

if __name__ == '__main__':
    basicNeoTest()