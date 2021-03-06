# -*- coding: utf-8 -*-
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
.. module:: r1
   :platform: r2
   :synopsis: r3

.. moduleauthor:: r4

"""

import unittest

import savu.test.test_utils as tu
from savu.test.plugin_runner_test import \
    run_protected_plugin_runner_no_process_list


class "r5"(unittest.TestCase):

    def "r6"(self):
        options = tu.set_experiment("r7")
        plugin = "r8"
        run_protected_plugin_runner_no_process_list(options, plugin)

if __name__ == "__main__":
    unittest.main()
