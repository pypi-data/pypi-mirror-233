# SPDX-FileCopyrightText: 2019,2020 Freemelt AB
#
# SPDX-License-Identifier: Apache-2.0

import collections
import collections.abc

# This monkey-patch fixes this warning:
# /usr/local/lib/python3.9/dist-packages/svg/path/path.py:3:
# DeprecationWarning: Using or importing the ABCs from 'collections'
# instead of from 'collections.abc' is deprecated since Python 3.3,
# and in 3.10 it will stop working
collections.MutableSequence = collections.abc.MutableSequence
