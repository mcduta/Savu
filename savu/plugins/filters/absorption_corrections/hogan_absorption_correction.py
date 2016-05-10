# Copyright 2014 Diamond Light Source Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
.. module:: HoganAbsorptionCorrection    
   :platform: Unix
   :synopsis: A plugin apply hogans xrf absorption correction using stxm data


.. moduleauthor:: Aaron D. Parsons <scientificsoftware@diamond.ac.uk>
"""

import numpy as np
import logging
from savu.plugins.filters.base_absorption_correction import BaseAbsorptionCorrection
from savu.plugins.utils import register_plugin


@register_plugin
class HoganAbsorptionCorrection(BaseAbsorptionCorrection):
    """
    Hogans absorption correction, takes in a normalised absorption sinogram and xrf sinogram stack

    """

    def __init__(self):
        logging.debug("Starting Hogan Absorption correction")
        super(HoganAbsorptionCorrection,
              self).__init__("HoganAbsorptionCorrection")
              
    def pre_process(self):
        compound = self.parameters['compound']
        density = self.parameters['density']
        mData = self.get_in_meta_data()[0]
        mono_energy = mData.get_meta_data('mono_energy')
        peak_energy = mData.get_meta_data('PeakEnergy')
        pump_mu = self.get_mu(compound, float(mono_energy), density)
        peak_mu = self.get_mu(compound, list(peak_energy), density)
        self.atten_ratio = [pm/pump_mu for pm in peak_mu]
        logging.debug('The test attenuation ratios should be:[25.651, 20.909, 2.903, 2.198],'
                            'they are: %s' % self.atten_ratio)
        theta = mData.get_meta_data('rotation_angle')
        self.dtheta = theta[1]-theta[0]
        logging.debug('The rotation step is %s' % str(self.dtheta))
        if np.abs(self.dtheta)>10.0:
            logging.warn('The theta step is greater than 10 degrees! Watch out!')
        self.npix_displacement = self.parameters['azimuthal_offset']//self.dtheta
        logging.debug('This gives a pixel offset of %s' % str(self.npix_displacement))
        

    def filter_frames(self, data):
        xrf = data[0]
        stxm_orig = data[1]
        logging.debug('the xrf shape is %s' % str(xrf.shape))
        logging.debug('the stxm shape is %s' % str(stxm_orig.shape))
        # take the log here, we assume it is monitor corrected already
        stxm = -np.log10(stxm_orig)
        # now correct for the rotation offset
        absorption = np.roll(stxm,int(self.npix_displacement), axis=0)
        num_channels = self.get_num_channels()
        corrected_xrf = np.zeros_like(xrf)
        for i in range(num_channels):
            fluo_sino = xrf[:,:,i]
            corrected_xrf[:,:,i], corr_fac = self.correct_sino(absorption, fluo_sino, self.atten_ratio[i])
            logging.debug('For channel %s, min correction: %s, max correction: %s' % (str(i),
                                                                                      str(np.min(corr_fac)),
                                                                                      str(np.max(corr_fac))))
        return corrected_xrf

    def correct_sino(self, stxm_sino, fluo_sino, atten_ratio):
        foo = np.arange(stxm_sino.shape[1]) + 1.0 * np.ones_like(abs)
        transmission_sum = np.cumsum(stxm_sino, axis=1)
        transmission_average = transmission_sum / foo
        exponent_Co = np.exp(-transmission_average * atten_ratio * stxm_sino)
        corrected_fluo_sino = exponent_Co * fluo_sino
        return corrected_fluo_sino, exponent_Co
