"""
tteamodel

A Python package for model in the T-TEA platform,
supporting data model description. Developed by the   team.

This package provides models for data representation and manipulation.

Attributes
----------
__version__ : str
    The current version of the package.
__date__ : str
    The release date of this version.
__author__ : str
    The development team.
__license__ : str
    The license under which the package is distributed.

See Also
--------
Language
    Model for managing language data.
Player
    Model for managing player data.

Notes
-----
This package is maintained by the   team and is under active
development. Contributions and bug reports are welcome at:
https://github.com/-/_ttea_view
"""

# Define the __all__ variable
__all__ = [
    "Language",
    "Player",
]

__version__ = "1.0.0"
__date__ = "2025-12-25"
__author__ = " "
__license__ = "MIT License"

# Import the submodules
from .language import Language
from .player import Player
