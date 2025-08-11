"""
udescjoinvilletteaview

A Python package for visualizing and editing data from the T-TEA platform,
supporting internationalization and player data management. Developed by the
Larva UDESC team.

This package provides tools for creating visualizations, managing player
profiles, and supporting multiple languages for the T-TEA platform.

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
AboutView
    Displays metadata and project information.
LanguageView
    Manages internationalization and locale formatting.
PlayerEditView
    Supports creation and editing of player profiles.
PlayerListView
    Lists player data in a structured format.
SplashScreen
    Displays a splash screen during application startup.

Notes
-----
This package is maintained by the Larva UDESC team and is under active
development. Contributions and bug reports are welcome at:
https://github.com/larva-udesc/udesc_ttea_view
"""

# Define the __all__ variable
__all__ = [
    "AboutView",
    "LanguageView",
    "PlayerEditView",
    "PlayerListView",
    "SplashScreen",
]

__version__ = "1.0.0"
__date__ = "2025-12-25"
__author__ = "Larva UDESC"
__license__ = "MIT License"

# Import the submodules
from .aboutview import AboutView
from .languageview import LanguageView
from .playereditview import PlayerEditView
from .playerlistview import PlayerListView
from .splashscreen import SplashScreen
