from __future__ import annotations

import contextlib
import pkgutil

from typing import Any, Literal
from urllib import parse

from mknodes.basenodes import mkcontainer, mknode
from mknodes.data import datatypes
from mknodes.info import packageregistry
from mknodes.templatenodes import mkbadge
from mknodes.utils import log, reprhelpers


logger = log.get_logger(__name__)


class MkMetadataBadges(mkcontainer.MkContainer):
    """Container node for a list of metadata badges.

    Badges are generated locally using "anybadge" package
    """

    ICON = "simple/shieldsdotio"
    STATUS = "new"

    def __init__(
        self,
        typ: datatypes.MetadataTypeStr,
        *,
        package: str | None = None,
        font_size: Literal[10, 11, 12] | None = None,
        font_name: str | None = None,
        num_padding_chars: int | None = None,
        badge_color: str | None = None,
        text_color: str | None = None,
        use_gitlab_style: bool = False,
        **kwargs: Any,
    ):
        """Constructor.

        Arguments:
            typ: Metadata badges to show
            package: Package to show badges for. If None, it will get pulled from project
            font_size: Size of font to use
            font_name: Name of font to use
            num_padding_chars: Number of chars to use for padding
            badge_color: Badge color. If none is set, it will be pulled from project.
            text_color: Badge color
            use_gitlab_style: Use Gitlab-scope style
            kwargs: Keyword arguments passed to parent
        """
        super().__init__(**kwargs)
        self.block_separator = "\n"
        self._package = package
        self._typ = typ
        self.font_size = font_size
        self.font_name = font_name
        self.num_padding_chars = num_padding_chars
        self.badge_color = badge_color
        self.text_color = text_color
        self.use_gitlab_style = use_gitlab_style

    def __repr__(self):
        return reprhelpers.get_repr(
            self,
            typ=self._typ,
            package=self._package,
            font_size=self.font_size,
            font_name=self.font_name,
            badge_color=self.badge_color,
            text_color=self.text_color,
            num_padding_chars=self.num_padding_chars,
            use_gitlab_style=self.use_gitlab_style,
            _filter_empty=True,
            _filter_false=True,
        )

    @property
    def badge_content(self) -> list[tuple]:
        items: list[tuple] = []
        ctx = (
            packageregistry.get_info(self._package)
            if self._package
            else self.ctx.metadata
        )
        match self._typ:
            case "classifiers":
                dct = ctx.classifier_map
                for category, labels in dct.items():
                    items.extend([(i, category, None) for i in labels])
            case "keywords":
                items.extend((keyword, "", None) for keyword in ctx.keywords)
            case "keywords_combined":
                items.append(("Keywords", " | ".join(ctx.keywords), None))
            case "required_python":
                string = ctx.required_python_version
                items.append(("Python", string, "https://www.python.org"))
            case "websites":
                urls = [
                    (name, parse.urlparse(url).netloc, url)
                    for name, url in ctx.urls.items()
                ]
                items.extend(urls)
            case "dependencies":
                info = ctx.required_packages
                items.extend(
                    (package.name, package.version, package.homepage) for package in info
                )
            case "installed_packages":
                pkgs = []
                for mod in pkgutil.iter_modules():
                    if not mod.ispkg:
                        continue
                    with contextlib.suppress(Exception):
                        dist = packageregistry.get_info(mod.name)
                        pkgs.append(dist)
                items.extend(
                    (package.name, package.version, package.homepage) for package in pkgs
                )
            case str():
                raise ValueError(self._typ)
            case _ if self._typ in datatypes.CLASSIFIERS:
                labels = ctx.classifier_map.get(self._typ, [])
                items.extend([(i, self._typ, None) for i in labels])
        return items

    @property
    def items(self) -> list[mknode.MkNode]:
        return [
            mkbadge.MkBadge(
                label=label,
                value=value,
                link=link,
                font_size=self.font_size,
                font_name=self.font_name,
                badge_color=self.badge_color,
                text_color=self.text_color,
                num_padding_chars=self.num_padding_chars,
                use_gitlab_style=self.use_gitlab_style,
                title=label,
                parent=self,
            )
            for label, value, link in self.badge_content
        ]

    @items.setter
    def items(self, value):
        pass

    @staticmethod
    def create_example_page(page):
        import mknodes as mk

        node = MkMetadataBadges(typ="classifiers")
        page += mk.MkReprRawRendered(node, header="### Classifiers")
        node = MkMetadataBadges(typ="keywords")
        page += mk.MkReprRawRendered(node, header="### Keywords")
        node = MkMetadataBadges(typ="keywords_combined")
        page += mk.MkReprRawRendered(node, header="### Keywords")
        node = MkMetadataBadges(typ="websites")
        page += mk.MkReprRawRendered(node, header="### Websites")
        node = MkMetadataBadges(typ="dependencies")
        page += mk.MkReprRawRendered(node, header="### Dependencies")
        node = MkMetadataBadges(typ="dependencies", package="mkdocs")
        page += mk.MkReprRawRendered(node, header="### For other package")
        # node = MkMetadataBadges(typ="installed_packages")
        # page += mk.MkReprRawRendered(node, header="### Installed packages")
        node = MkMetadataBadges(typ="classifiers", use_gitlab_style=True)
        page += mk.MkReprRawRendered(node, header="### Gitlab style")
        node = MkMetadataBadges(typ="required_python", badge_color="red")
        page += mk.MkReprRawRendered(node, header="### Colored")


if __name__ == "__main__":
    node = MkMetadataBadges.with_default_context("websites")
    print(node)
