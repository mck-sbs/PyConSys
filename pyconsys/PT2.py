# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from pyconsys.Control import Control


class PT2(Control):

    def __init__(self, a2, a1, a0, b0):
        self._a2 = a2
        self._a1 = a1
        self._a0 = a0
        self._b0 = b0
        self._xa_old1 = 0
        self._xa_old2 = 0

    def reset(self):
        self._xa_old1 = 0
        self._xa_old2 = 0

    def get_xa(self, xe):
        xa = (self._b0 * xe
              + ((2 * self._a2 * self._xa_old1 - self._a2 * self._xa_old2) / (self.DELTA_T * self.DELTA_T))
              + ((self._a1 * self._xa_old1) / self.DELTA_T)) / \
             ((self._a2 / (self.DELTA_T * self.DELTA_T)) + (self._a1 / self.DELTA_T) + self._a0)

        self._xa_old2 = self._xa_old1
        self._xa_old1 = xa
        return xa
