# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


class Control():
    """ This should be an abstract class. Do not instantiate."""
    DELTA_T = 0.01

    def get_xa(self, xe):
        raise NotImplementedError()
