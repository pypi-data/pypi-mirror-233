# -*- coding: utf-8 -*-
# Copyright (C) 2022 Cardiff University

"""IGWN extensions for Sphinx-Immaterial
"""

from pathlib import Path

import sphinx_immaterial

from .defaults import (
    DEFAULT_HTML_LOGO,
    DEFAULT_HTML_FAVICON,
    DEFAULT_THEME_OPTIONS,
)

try:  # parse version
    from ._version import version as __version__
except ModuleNotFoundError:  # development mode
    __version__ = ''

__author__ = "Duncan Macleod <duncan.macleod@ligo.org>"
__license__ = "MIT"

HERE = Path(__file__).parent.absolute()

sphinx_immaterial.DEFAULT_THEME_OPTIONS.update(DEFAULT_THEME_OPTIONS)


def _default_config(app, config):
    """Update default config.
    """
    if "html_logo" not in config or not config["html_logo"]:
        config["html_logo"] = DEFAULT_HTML_LOGO
    if "html_favicon" not in config or not config["html_favicon"]:
        config["html_favicon"] = DEFAULT_HTML_FAVICON
    return


def setup(app):
    out = sphinx_immaterial.setup(app)
    app.connect("config-inited", _default_config)
    app.add_html_theme(
        "sphinx_immaterial_igwn",
        str(Path(__file__).parent.absolute()),
    )
    return out
