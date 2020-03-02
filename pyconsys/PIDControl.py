# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from pyconsys.PControl import PControl
from pyconsys.IControl import IControl
from pyconsys.DControl import DControl


class PIDControl():
    """ PID controller """
    def __init__(self, kp, ki, kd):
        """ set Kp, Ki, Kd
        Parameters:
        kp(float): Kp
        ki(float): Ki
        kd(float): Kd """
        self._pControl = PControl(kp)
        self._iControl = IControl(ki)
        self._dControl = DControl(kd)

    def update_params(self, kp, ki, kd):
        """ update Kp, Ki, Kd
        Parameters:
        kp(float): Kp
        ki(float): Ki
        kd(float): Kd """
        self._pControl.reset(kp)
        self._iControl.reset(ki)
        self._dControl.reset(kd)

    def get_xa(self, xe):
        """ give input, get output
        Parameters:
        xe(float): input xe

        Returns:
        float: output xa """
        xa = self._pControl.get_xa(xe) + self._iControl.get_xa(xe) + self._dControl.get_xa(xe)
        return xa
