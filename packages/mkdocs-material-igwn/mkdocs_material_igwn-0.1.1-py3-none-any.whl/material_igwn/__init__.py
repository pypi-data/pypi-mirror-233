# -*- coding: utf-8 -*-

"""IGWN extensions for MkDocs for Material.
"""

__author__ = "Duncan Macleod <duncan.macleod@ligo.org>"
__license__ = "MIT"

try:  # parse version
    from ._version import version as __version__
except ModuleNotFoundError:  # development mode
    __version__ = ''
