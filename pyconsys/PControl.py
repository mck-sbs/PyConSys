# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from pyconsys.Control import Control


class PControl(Control):

    def __init__(self, kp):
        self._kp = kp

    def get_xa(self, xe):
        return xe * self._kp
