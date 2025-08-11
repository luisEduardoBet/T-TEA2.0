"""
udescjoinvilletteaapp

A Python package for application management
in the T-TEA platform. Developed by the Larva UDESC team.

This package provides tools for for application
management for the T-TEA platform.

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
AppConfig
    Manages application configuration settings.
TTeaApp
    Main application class for the T-TEA platform.

Notes
-----
This package is maintained by the Larva UDESC team and is under active
development. Contributions and bug reports are welcome at:
https://github.com/larva-udesc/udesc_ttea_view
"""

# Define the __all__ variable
__all__ = [
    "AppConfig",
    "TTeaApp",
]

__version__ = "1.0.0"
__date__ = "2025-12-25"
__author__ = "Larva UDESC"
__license__ = "MIT License"

# Import the submodules
from .appconfig import AppConfig
from .tteaapp import TTeaApp
