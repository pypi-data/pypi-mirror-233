# -*- coding: utf-8 -*-
# Copyright (C) 2022 Cardiff University

"""sphinx-immaterial theme default overrides for IGWN.
"""

__author__ = "Duncan Macleod <duncan.macleod@ligo.org>"

from pathlib import Path

HERE = Path(__file__).parent.absolute()

IMAGES_PATH = HERE / "static" / "images"
DEFAULT_HTML_LOGO = str(IMAGES_PATH / "logo.png")

DEFAULT_HTML_FAVICON = str(IMAGES_PATH / "favicon.ico")

DEFAULT_THEME_OPTIONS = {
    # default features
    "features": [
        "navigation.expand",
        "navigation.sections",
    ],

    # logos

    # default palette to include light/dark detection
    "palette": [
        {
            "media": "(prefers-color-scheme: light)",
            "scheme": "igwn",
            "toggle": {
                "icon": "material/eye-outline",
                "name": "Switch to dark mode",
            },
        },
        {
            "media": "(prefers-color-scheme: dark)",
            "scheme": "slate",
            "primary": "orange",
            "accent": "orange",
            "toggle": {
                "icon": "material/eye",
                "name": "Switch to light mode",
            },
        },
    ],
}
