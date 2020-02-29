# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from pyconsys.Control import Control


class PT2(Control):

    def __init__(self, a2, a1, a0, b0):
        """ set a2y2(t) + a1y1(t) + a0y0(t) = b0u(t)
        Parameters:
        a2(float): a2
        a1(float): a1
        a0(float): a0
        b0(float): bo """
        self._a2 = a2
        self._a1 = a1
        self._a0 = a0
        self._b0 = b0
        self._xa_old1 = 0
        self._xa_old2 = 0

    def reset(self):
        """ resets the unit """
        self._xa_old1 = 0
        self._xa_old2 = 0

    def get_xa(self, xe):
        """ give input, get output
        Parameters:
        xe(float): input xe

        Returns:
        float: output xa """
        xa = (self._b0 * xe
              + ((2 * self._a2 * self._xa_old1 - self._a2 * self._xa_old2) / (self.DELTA_T * self.DELTA_T))
              + ((self._a1 * self._xa_old1) / self.DELTA_T)) / \
             ((self._a2 / (self.DELTA_T * self.DELTA_T)) + (self._a1 / self.DELTA_T) + self._a0)

        self._xa_old2 = self._xa_old1
        self._xa_old1 = xa
        return xa
