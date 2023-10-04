# Copyright (c) 2016-2023 Association of Universities for Research in Astronomy, Inc. (AURA)
# For license information see LICENSE or https://opensource.org/licenses/BSD-3-Clause

"""
A small version of GPP data model
"""
from typing import NewType

from .atom import *
from .constraints import *
from .group import *
from .ids import *
from .magnitude import *
from .observation import *
from .observationmode import *
from .program import *
from .qastate import *
from .resource import *
from .semester import *
from .site import *
from .target import *
from .timeallocation import *
from .timingwindow import *
from .too import *
from .wavelength import *

# Type alias for a night index.
NightIndex = NewType('NightIndex', int)

# Type alias for multiple night indices.
NightIndices = npt.NDArray[NightIndex]
