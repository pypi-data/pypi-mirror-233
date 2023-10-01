import mknodes as mk

from mknodes.theme import materialtheme


def build(project: mk.Project[materialtheme.MaterialTheme]):
    nav = project.get_root()
    index_page = nav.add_index_page(hide="toc")
    index_page += "## Sub-Pages"
    websites = dict(
        ruff="https://github.com/astral-sh/ruff.git",
        MkDocStrings="https://github.com/mkdocstrings/mkdocstrings.git",
        MkDocs="https://github.com/mkdocs/mkdocs.git",
    )
    for k, v in websites.items():
        subproject = mk.Project.for_path(v)
        website_nav = mk.MkDefaultWebsite(section=k, project=subproject)
        nav += website_nav
        index_page += mk.MkLink(target=website_nav, title=k, icon="link")
