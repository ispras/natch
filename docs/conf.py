# Sphinx configuration

project = "Natch"
copyright = "ISPRAS"
author = "ISPRAS"

extensions = [
"myst_parser",
]

# Markdown support

source_suffix = {
".md": "markdown",
}

# Allow Markdown headings to be referenced.

myst_heading_anchors = 3

# Templates and static files

templates_path = ["_templates"]
html_static_path = ["_static"]

exclude_patterns = [
"_build",
"Thumbs.db",
".DS_Store",
]

# HTML theme

html_theme = "sphinx_rtd_theme"
html_title = "Natch documentation"

# Show "View page source" in the upper-right corner.

html_show_sourcelink = True

# Don't put the .md extension into generated links.

html_link_suffix = ".html"

# Language of the documentation content.

language = "ru"
