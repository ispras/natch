import sys
from pathlib import Path

project = "Natch"
copyright = "ISPRAS"
author = "ISPRAS"

# sys.path.insert(0, str(Path(__file__).parent / "_ext"))

extensions = [
    "myst_parser",
    "sphinx_multitoc_numbering",
    "sphinx_design",
]

myst_enable_extensions = [
    "html_image",  # Позволяет Sphinx распознавать и копировать HTML-картинки
    "colon_fence",
]

# Sphinx configuration


# Markdown support

source_suffix = {
    ".md": "markdown",
}

# Allow Markdown headings to be referenced.

myst_heading_anchors = 3

# Templates and static files

templates_path = ["_templates"]
html_static_path = ["_static"]
html_css_files = ["custom.css"]

exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
]

# HTML theme

html_theme = "sphinx_rtd_theme"
html_title = "Natch documentation"
html_logo  = "_static/logo.png"

# Show "View page source" in the upper-right corner.

html_show_sourcelink = True

# Don't put the .md extension into generated links.

html_link_suffix = ".html"

# Language of the documentation content.

language = "ru"
