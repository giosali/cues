# -*- coding: utf-8 -*-

# 8888888b.                                         888
# 888   Y88b                                        888
# 888    888                                        888
# 888   d88P 888d888 .d88b.  88888b.d88b.  88888b.  888888 .d8888b
# 8888888P"  888P"  d88""88b 888 "888 "88b 888 "88b 888    88K
# 888        888    888  888 888  888  888 888  888 888    "Y8888b.
# 888        888    Y88..88P 888  888  888 888 d88P Y88b.       X88
# 888        888     "Y88P"  888  888  888 88888P"   "Y888  88888P'
#                                          888
#                                          888
#                                          888

"""
The Prompts Library
===================

:copyright: (c) 2021 by Giovanni Salinas
:license: MIT
"""

import sys

from .__version__ import (
    __title__, __version__, __author__, __author_email__,
    __description__, __url__, __license__, __copyright__
)
if '-m' not in sys.argv:
    from .checkbox import Checkbox
    from .confirm import Confirm
    from .form import Form
    from .select import Select
    from .survey import Survey
