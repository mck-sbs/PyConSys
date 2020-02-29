# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from pyconsys.Control import Control


class PT1(Control):
    """ PT1 unit """
    def __init__(self, p=1, t=0.01):
        """ set P and tau
        Parameters:
        p(float): P
        t(float): tau """
        self._p = p
        self._t = t
        self._xa_old = 0

    def reset(self):
        """ resets the unit """
        self._xa_old = 0

    def get_xa(self, xe):
        """ give input, get output
        Parameters:
        xe(float): input xe

        Returns:
        float: output xa """
        xa = (self._p * xe * self.DELTA_T + self._t * self._xa_old) / (self._t + self.DELTA_T)
        self._xa_old = xa
        return xa
