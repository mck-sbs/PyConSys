# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from pyconsys.Control import Control


class PT1(Control):

    def __init__(self, p, t):
        self._p = p
        self._t = t
        self._xa_old = 0

    def get_xa(self, xe):
        xa = (self._p * xe * self.DELTA_T + self._t * self._xa_old) / (self._t + self.DELTA_T)
        self._xa_old = xa
        return xa
