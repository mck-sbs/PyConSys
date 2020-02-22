# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from pyconsys.PControl import PControl
from pyconsys.IControl import IControl
from pyconsys.DControl import DControl


class PIDControl():
    def __init__(self, kp, ki, kd):
        self._pControl = PControl(kp)
        self._iControl = IControl(ki)
        self._dControl = DControl(kd)

    def get_xa(self, xe):
        xa = self._pControl.get_xa(xe) + self._iControl.get_xa(xe) + self._dControl.get_xa(xe)
        return xa
