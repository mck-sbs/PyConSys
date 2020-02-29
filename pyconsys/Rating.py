# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import numpy as np
from math import isnan


class Rating():
    """ rates the quality of control curves """
    def __init__(self):
        self._chunk_size = 100
        self._lst = []
        self._w = 0

    def get_update_rating(self, lst, w):
        """ give input, get output
        Parameters:
        lst(list): list of x values
        w(float): the w value of the loop

        Returns:
        float: rating """
        self._lst = lst
        self._w = w
        ret = self._get_rating()
        return ret

    def _get_rating(self):

        osc = self._get_oscillate_rating() * 5
        ovr = self._get_overflow_rating() * 20
        dst = abs(100 - self._get_distance_rating(self._lst, self._w)) * 20
        tm = self._get_timetoreach_rating() * 5
        rate_raw = osc + ovr + dst + tm
        rat = 1000 - rate_raw
        if rat < 0 or isnan(rat):
            rat = 0
        return rat

    def _get_oscillate_rating(self):
        arr = np.asarray(self._lst)
        arrs = np.array_split(arr, self._chunk_size)
        i = 0
        rat_old = 0
        incr = True

        for ar in arrs:
            rat = self._get_distance_rating(ar, self._w)
            if rat > rat_old:
                if not incr:
                    i = i + 1
                    incr = True

            if rat < rat_old:
                if incr:
                    i = i + 1
                    incr = False

            rat_old = rat
        return i

    def _get_overflow_rating(self):
        mx = max(self._lst)
        ret = (mx / self._w) * 100 - 100
        return ret

    def _get_distance_rating(self, lst, w):

        mean = np.asarray(lst).mean()
        ret = (mean / w) * 100
        return ret

    def _get_timetoreach_rating(self):
        arr = np.asarray(self._lst)
        arrs = np.array_split(arr, self._chunk_size)
        i = 0
        for ar in arrs:
            i = i + 1
            rat = self._get_distance_rating(ar, self._w)

            if abs(rat - 100) < 5:
                break
        return i
