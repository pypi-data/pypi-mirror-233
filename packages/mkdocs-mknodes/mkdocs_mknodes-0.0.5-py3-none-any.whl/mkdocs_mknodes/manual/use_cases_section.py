import mknodes as mk

from mknodes.info import mkdocsconfigfile


nav = mk.MkNav("Use cases")


def create_use_cases_section(root_nav: mk.MkNav):
    """Create the "Development" sub-MkNav."""
    root_nav += nav
    page = nav.add_index_page(hide="toc")
    page += mk.MkJinjaTemplate("use_cases_index.jinja")
    page.created_by = create_use_cases_section


@nav.route.page("Creating a sample website", hide="toc")
def create_default_website_section(page: mk.MkPage):
    """Create the "Creating a sample website" MkPage."""
    file = mkdocsconfigfile.MkDocsConfigFile("configs/mkdocs_mkdocs.yml")
    section = file.get_section("plugins", "mknodes", keep_path=True)
    config = section.serialize("yaml")
    variables = dict(config=config)
    page += mk.MkJinjaTemplate("use_case_default_website.jinja", variables=variables)


@nav.route.page("Creating a website via config", hide="toc")
def create_custom_website_by_config(page: mk.MkPage):
    """Create the "Creating a sample website via config" MkPage."""
    file = mkdocsconfigfile.MkDocsConfigFile("configs/mkdocs_mkdocstrings.yml")
    section = file.get_section("plugins", "mknodes", keep_path=True)
    config = section.serialize("yaml")
    variables = dict(config=config)
    page += mk.MkJinjaTemplate("use_case_by_config.jinja", variables=variables)
