# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# 2020, Metin Karatas (m.karatas@sbs-herzogenaurach.de)

from pyconsys.Control import Control


class DControl(Control):

    def __init__(self, kd):
        self._kd = kd
        self._xe_old = 0

    def get_xa(self, xe):
        xa = self._kd * ((xe - self._xe_old) / self.DELTA_T)
        self._xe_old = xe
        return xa
