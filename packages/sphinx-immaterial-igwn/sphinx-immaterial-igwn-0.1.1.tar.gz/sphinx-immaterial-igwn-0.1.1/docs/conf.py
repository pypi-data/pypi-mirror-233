# -*- coding: utf-8 -*-
# Copyright (C) 2022 Cardiff University

"""Documentation configuration for sphinx-immaterial-igwn
"""

from sphinx_immaterial_igwn import __version__

# metadata
project = "sphinx-immaterial-igwn"
copyright = "2022 Cardiff University"
author = "Duncan Macleod"
if "dev" in __version__:
    release = version = "dev"
else:
    release = version = __version__

# config
default_role = "obj"
extensions = [
    "sphinx_immaterial_igwn",
]

# theme
html_theme = "sphinx_immaterial_igwn"
html_theme_options = {
    "edit_uri": "blob/main/sphinx/docs",
    "repo_name": "igwn-material",
    "repo_url": "https://git.ligo.org/computing/igwn-material",
    "repo_type": "gitlab",
    "site_url": "https://computing.docs.ligo.org/igwn-material/sphinx/",
}
html_last_updated_fmt = ""
