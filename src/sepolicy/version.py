"""
Version Module

Version information.
"""

__version__ = "1.0.0"
__author__ = "XTENSEI"
__description__ = "Android SELinux Policy Patcher"


def get_version():
    """Return version string."""
    return __version__


def get_info():
    """Return version info dict."""
    return {
        "version": __version__,
        "author": __author__,
        "description": __description__,
    }
