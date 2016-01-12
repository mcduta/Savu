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
.. module:: filter
   :platform: Unix
   :synopsis: A base class for all standard filters

.. moduleauthor:: Mark Basham <scientificsoftware@diamond.ac.uk>

"""
from savu.plugins.base_filter import BaseFilter
from savu.plugins.driver.cpu_plugin import CpuPlugin


class BaseComponentAnalysis(BaseFilter, CpuPlugin):
    """
    A base plugin for doing component analysis. This sorts out the main features
    of a component analysis
    :param in_datasets: A list of the dataset(s) to process. Default: [].
    :param out_datasets: A list of the dataset(s) to process. Default: ['scores', 'eigenvectors'].
    :param number_of_components: The number expected components. Default: 3.
    :param chunk: The chunk to work on. Default: 'SINOGRAM'.
    :param whiten: To subtract the mean or not. Default: 1.
    """

    def __init__(self, name):
        super(BaseComponentAnalysis, self).__init__(name)

    def get_max_frames(self):
        return self.spectra_length

    def get_plugin_pattern(self):
        return self.parameters['chunk']

    def setup(self):
        self.exp.log(self.name + " Setting up the component analysis")
        # set up the output dataset that is created by the plugin
        in_dataset, out_dataset = self.get_datasets()
        self.spectra_length = (in_dataset[0].get_shape()[-1],)
        other_dims = in_dataset[0].get_shape()[:-1]
        num_comps = (self.parameters['number_of_components'],)
        self.images_shape = other_dims + num_comps
        components_shape = num_comps + self.spectra_length
        # copy all required information from in_dataset[0]
        out_dataset[0].create_dataset(in_dataset[0])
        out_dataset[0].set_shape(self.images_shape)

        axis_labels = ['idx.unit', 'spectra.unit']
        out_dataset[1].create_dataset(shape=components_shape,
                                      axis_labels=axis_labels)
        spectrum = {'core_dir': (1,), 'slice_dir': (0,)}
        out_dataset[1].add_pattern("SPECTRUM", **spectrum)
        in_pData, out_pData = self.get_plugin_datasets()
        plugin_pattern = self.get_plugin_pattern()
        in_pData[0].plugin_data_setup(plugin_pattern, self.get_max_frames()) 
        out_pData[0].plugin_data_setup(plugin_pattern, num_comps)
        out_pData[1].plugin_data_setup("SPECTRUM", num_comps)
        self.exp.log(self.name + " End")

    def nInput_datasets(self):
        return 1

    def nOutput_datasets(self):
        return 2
