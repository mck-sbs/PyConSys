# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from pyconsys.Control import Control


class IControl(Control):
    """ I control unit"""
    def __init__(self, ki=1):
        """ set Ki
        Parameters:
        ki(float): Ki """
        self._ki = ki
        self._sum = 0

    def reset(self, ki):
        """ resets the unit """
        self._ki = ki
        self._sum = 0

    def get_xa(self, xe):
        """ give input, get output
        Parameters:
        xe(float): input xe

        Returns:
        float: output xa """
        self._sum = self._sum + xe
        return self._ki * self._sum * self.DELTA_T
