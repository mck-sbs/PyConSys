# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from pyconsys.Control import Control


class DControl(Control):
    """ D control unit """
    def __init__(self, kd=1):
        """ set Kd
        Parameters:
        kd(float): Kd """
        self._kd = kd
        self._xe_old = 0

    def reset(self, kd):
        """ resets the unit """
        self._kd = kd
        self._xe_old = 0

    def get_xa(self, xe):
        """ give input, get output
        Parameters:
        xe(float): input xe

        Returns:
        float: output xa """
        xa = self._kd * ((xe - self._xe_old) / self.DELTA_T)
        self._xe_old = xe
        return xa
