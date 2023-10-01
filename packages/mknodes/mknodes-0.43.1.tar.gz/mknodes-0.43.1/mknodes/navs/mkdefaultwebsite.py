from __future__ import annotations

import mknodes as mk

from mknodes.utils import log


logger = log.get_logger(__name__)


class MkDefaultWebsite(mk.MkNav):
    """Nav for showing a module documenation."""

    def __init__(
        self,
        static_pages: dict[str, str | dict | list] | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        page = self.add_index_page("Overview", hide="toc")
        page += mk.MkText(page.ctx.metadata.description)
        static_pages = static_pages or {}
        self.parse.json(static_pages)
        docs = self.add_doc(section_name="API")
        docs.collect_classes(recursive=True)
        if proj := self.associated_project:
            proj.theme.announcement_bar = mk.MkMetadataBadges("websites")
        if self.ctx.metadata.cli:
            page = self.add_page("CLI", hide="nav")
            page += mk.MkClickDoc(show_subcommands=True)

        nav = self.add_nav("Development")

        page = nav.add_page("Changelog")
        page += mk.MkChangelog()

        page = nav.add_page("Code of conduct")
        page += mk.MkCodeOfConduct()

        page = nav.add_page("Contributing")
        page += mk.MkCommitConventions()
        page += mk.MkPullRequestGuidelines()

        page = nav.add_page("Setting up the environment")
        page += mk.MkDevEnvSetup()
        page += mk.MkDevTools(header="Tools")

        page = nav.add_page("Dependencies")
        page += mk.MkDependencyTable()
        page += mk.MkPipDepTree(direction="LR")

        page = nav.add_page("Module overview")
        page += mk.MkModuleOverview()

        if "mkdocs.plugins" in self.ctx.metadata.entry_points:
            page = nav.add_page("MkDocs Plugins")
            page += mk.MkPluginFlow()

        node = mk.MkLicense()
        page = nav.add_page("License", hide="toc")
        page += node

    @classmethod
    def for_project(cls, project, **kwargs):
        root = cls(project=project, **kwargs)
        project.set_root(root)
        return root


if __name__ == "__main__":
    doc = MkDefaultWebsite.for_project(
        mk.Project.for_mknodes(),
        static_pages={
            "Usage": "https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/getting-started.md",
        },
    )
    print(doc)
