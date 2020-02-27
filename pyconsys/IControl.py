# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from pyconsys.Control import Control


class IControl(Control):

    def __init__(self, ki):
        self._ki = ki
        self._sum = 0

    def get_xa(self, xe):
        self._sum = self._sum + xe
        return self._ki * self._sum * self.DELTA_T

