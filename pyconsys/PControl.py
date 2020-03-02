# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from pyconsys.Control import Control


class PControl(Control):
    """ I control unit"""
    def __init__(self, kp=1):
        """set Kp
        Parameters:
        kp(float): Kp"""
        self._kp = kp

    def reset(self, kp):
        """ resets the unit """
        self._kp = kp

    def get_xa(self, xe):
        """ give input, get output
        Parameters:
        xe(float): input xe

        Returns:
        float: output xa """
        return xe * self._kp
