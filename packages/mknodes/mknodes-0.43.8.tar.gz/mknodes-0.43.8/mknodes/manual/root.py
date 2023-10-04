import mknodes as mk

from mknodes import manual
from mknodes.manual import get_started_section
from mknodes.theme import materialtheme


def build(project: mk.Project[materialtheme.MaterialTheme]) -> mk.MkNav:
    project.theme.error_page.content = mk.MkAdmonition("Page does not exist!")
    project.theme.content_area_width = 1300
    project.theme.tooltip_width = 800
    project.linkprovider.add_inv_file("https://mkdocstrings.github.io/objects.inv")

    root_nav = project.get_root()
    root_nav.page_template.announcement_bar = mk.MkMetadataBadges("websites")
    nav = get_started_section.nav
    root_nav += nav
    manual.create_navs_section(root_nav)
    manual.create_page_section(root_nav)
    manual.create_nodes_section(root_nav)
    manual.create_templating_section(root_nav)
    manual.create_development_section(root_nav)
    return root_nav
