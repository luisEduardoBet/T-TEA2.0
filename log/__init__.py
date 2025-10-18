"""
ttealog

A Python package for log functions in the T-TEA platform,
supporting logging. Developed by the   team.

This package provides tools for logging.

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
Log
    Provides logging functionality for the application.


Notes
-----
This package is maintained by the   team and is under active
development. Contributions and bug reports are welcome at:
https://github.com/-/_ttea_view
"""

# Define the __all__ variable
__all__ = [
    "Log",
]

__version__ = "1.0.0"
__date__ = "2025-12-25"
__author__ = " "
__license__ = "MIT License"

# Import the submodules
from .log import Log
