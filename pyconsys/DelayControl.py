# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import queue
from pyconsys.Control import Control


class DelayControl(Control):
    """ Delay control unit """
    def __init__(self, delay=0):
        """ set delay
        Parameters:
        delay(int): delay """
        self._delay = delay
        self._queue = queue.Queue()
        self._counter = 0

    def reset(self, delay):
        """ resets the unit """
        self._delay = delay
        self._counter = 0
        self._queue.queue.clear()

    def get_xa(self, xe):
        """ give input, get output
        Parameters:
        xe(float): input xe

        Returns:
        float: output xa """
        self._counter = self._counter + 1
        self._queue.put(xe)
        if self._counter > self._delay:
            xa = self._queue.get()
        else:
            xa = 0
        return xa
