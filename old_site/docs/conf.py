# import sys
from pathlib import Path

project = "Natch"
copyright = "ISPRAS"
author = "ISPRAS"

# sys.path.insert(0, str(Path(__file__).parent / "_ext"))

extensions = [
    "myst_parser",
    "sphinx_multitoc_numbering",
    "sphinx_design",
    "sphinx_multiversion",
]

myst_enable_extensions = [
    "html_image",
    "colon_fence",
]

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


html_sidebars = {
    "**": [
        "localtoc.html",
        "relations.html",
        "sourcelink.html",
        "searchbox.html",
    ],
}


# # Принудительно внедряем наш шаблон версий в разметку темы Read the Docs
# html_context = {
#     'extra_nav_items': [
#         # Этот трюк заставляет Sphinx отрендерить наш шаблон внутри сайдбара
#         '<!--include_versioning-->',
#     ]
# }

# # Переопределяем встроенный шаблон темы, чтобы подключить наш файл
# def setup(app):
#     app.config.html_context['extra_nav_items'] = ['versioning.html']



# settins for sphinx-multiversion

smv_branch_whitelist = r'^main$'

# only for 3.4.1 and above
# smv_tag_whitelist = r'^natch_docs_v\.(3\.4\.[1-9]\d*|3\.[5-9]\d*(\.\d+)?|[4-9]\d*(\.\d+)?)$'
smv_tag_whitelist = r'^natch_docs_v\.?3\.(4\.[1-9][0-9]*|[5-9][0-9]*(\.[0-9]+)?)$'

smv_released_pattern = r'^tags/.*$'

master_doc = 'index'



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
