from __future__ import annotations

import re

from typing import Any

from mknodes.utils import log


_MAXCACHE = 20

logger = log.get_logger(__name__)


# based on anyTree resolver, credits to them.


class BaseResolver:
    _match_cache: dict[tuple[str, bool], re.Pattern] = {}

    def __init__(self, ignore_case: bool = False):
        """Base resolver. Subclass to get glob functionality.

        Keyword Args:
            name (str): Name of the node attribute to be used for resolving
            ignore_case (bool): Enable case insensisitve handling.
        """
        super().__init__()
        self.ignore_case = ignore_case

    def get_parent(self, node):
        return NotImplemented

    def get_children(self, node):
        return NotImplemented

    def get_attribute(self, node):
        return NotImplemented

    def get_root(self, node):
        prev = node
        while node:
            node = self.get_parent(node)
            prev = node
        return prev

    def get_separator(self, node) -> str:
        return "/"

    def get(self, path: str, root_node):
        """Return instance at `path`.

        An example module tree:

        >>> top = Node("top", parent=None)
        >>> sub0 = Node("sub0", parent=top)
        >>> sub0sub0 = Node("sub0sub0", parent=sub0)
        >>> sub0sub1 = Node("sub0sub1", parent=sub0)
        >>> sub1 = Node("sub1", parent=top)

        A resolver using the `name` attribute:

        >>> r = Resolver('name')

        Relative paths:

        >>> r.get(top, "sub0/sub0sub0")
        Node('/top/sub0/sub0sub0')
        >>> r.get(sub1, "..")
        Node('/top')
        >>> r.get(sub1, "../sub0/sub0sub1")
        Node('/top/sub0/sub0sub1')
        >>> r.get(sub1, ".")
        Node('/top/sub1')
        >>> r.get(sub1, "")
        Node('/top/sub1')
        >>> r.get(top, "sub2")
        Traceback (most recent call last):
          ...
        ChildResolverError: Node('/top') has no child sub2.
        Children are: 'sub0', 'sub1'.

        Absolute paths:

        >>> r.get(sub0sub0, "/top")
        Node('/top')
        >>> r.get(sub0sub0, "/top/sub0")
        Node('/top/sub0')
        >>> r.get(sub0sub0, "/")
        Traceback (most recent call last):
          ...
        ResolverError: root node missing. root is '/top'.
        >>> r.get(sub0sub0, "/bar")
        Traceback (most recent call last):
          ...
        ResolverError: unknown root node '/bar'. root is '/top'.

        Going above the root node raises a :any:`RootResolverError`:

        >>> r.get(top, "..")
        Traceback (most recent call last):
            ...
        RootResolverError: Cannot go above root node Node('/top')

        Case insensitive matching:

        >>> r.get(top, '/TOP')
        Traceback (most recent call last):
            ...
        ResolverError: unknown root node '/TOP'. root is '/top'.

        >>> r = Resolver('name', ignore_case=True)
        >>> r.get(top, '/TOp')
        Node('/top')
        """
        node, parts = self._start(root_node, path, self.__cmp)
        for part in parts:
            if part == "..":
                parent = self.get_parent(node)
                if parent is None:
                    raise RootResolverError(node)
                node = parent
            elif part not in ("", "."):
                node = self._get(node, part)
        return node

    def _get(self, node, name):
        for child in self.get_children(node):
            if self.__cmp(self.get_attribute(child), str(name)):
                return child
        names = [repr(self.get_attribute(c)) for c in self.get_children(node)]
        raise ChildResolverError(node, name, names)

    def glob(self, path: str, root_node):
        """Return instances at `path` supporting wildcards.

        Behaves identical to :any:`get`, but accepts wildcards and returns
        a list of found nodes.

        * `*` matches any characters, except '/'.
        * `?` matches a single character, except '/'.

        An example module tree:

        >>> top = Node("top", parent=None)
        >>> sub0 = Node("sub0", parent=top)
        >>> sub0sub0 = Node("sub0", parent=sub0)
        >>> sub0sub1 = Node("sub1", parent=sub0)
        >>> sub1 = Node("sub1", parent=top)
        >>> sub1sub0 = Node("sub0", parent=sub1)

        A resolver using the `name` attribute:

        >>> r = Resolver('name')

        Relative paths:

        >>> r.glob(top, "sub0/sub?")
        [Node('/top/sub0/sub0'), Node('/top/sub0/sub1')]
        >>> r.glob(sub1, ".././*")
        [Node('/top/sub0'), Node('/top/sub1')]
        >>> r.glob(top, "*/*")
        [Node('/top/sub0/sub0'), Node('/top/sub0/sub1'), Node('/top/sub1/sub0')]
        >>> r.glob(top, "*/sub0")
        [Node('/top/sub0/sub0'), Node('/top/sub1/sub0')]
        >>> r.glob(top, "sub1/sub1")
        Traceback (most recent call last):
            ...
        ChildResolverError: Node('/top/sub1') has no child sub1.
        Children are: 'sub0'.

        Non-matching wildcards are no error:

        >>> r.glob(top, "bar*")
        []
        >>> r.glob(top, "sub2")
        Traceback (most recent call last):
          ...
        ChildResolverError: Node('/top') has no child sub2.
        Children are: 'sub0', 'sub1'.

        Absolute paths:

        >>> r.glob(sub0sub0, "/top/*")
        [Node('/top/sub0'), Node('/top/sub1')]
        >>> r.glob(sub0sub0, "/")
        Traceback (most recent call last):
          ...
        ResolverError: root node missing. root is '/top'.
        >>> r.glob(sub0sub0, "/bar")
        Traceback (most recent call last):
          ...
        ResolverError: unknown root node '/bar'. root is '/top'.

        Going above the root node raises a :any:`RootResolverError`:

        >>> r.glob(top, "..")
        Traceback (most recent call last):
            ...
        RootResolverError: Cannot go above root node Node('/top')
        """
        node, parts = self._start(root_node, path, self.__match)
        return self._glob(node, parts)

    def _start(self, node, path: str, cmp_) -> tuple[Any, list[str]]:
        sep = self.get_separator(node)
        parts = path.split(sep)
        # resolve root
        if path.startswith(sep):
            node = self.get_root(node)
            rootpart = self.get_attribute(node)
            parts.pop(0)
            if not parts[0]:
                msg = f"root node missing. root is '{sep}{rootpart}'."
                raise ResolverError(node, "", msg)
            if not cmp_(rootpart, parts[0]):
                msg = f"unknown root node '{sep}{parts[0]}'. root is '{sep}{rootpart}'."
                raise ResolverError(node, "", msg)
            parts.pop(0)
        return node, parts

    def _glob(self, node, parts):
        assert node is not None
        nodes = []
        if parts:
            name = parts[0]
            remainder = parts[1:]
            # handle relative
            if name == "..":
                parent = self.get_parent(node)
                if parent is None:
                    raise RootResolverError(node)
                nodes += self._glob(parent, remainder)
            elif name in ("", "."):
                nodes += self._glob(node, remainder)
            elif (matches := self._find(node, name, remainder)) or self.is_wildcard(name):
                nodes += matches
            else:
                names = [repr(self.get_attribute(c)) for c in self.get_children(node)]
                raise ChildResolverError(node, name, names)
        else:
            nodes = [node]
        return nodes

    def _find(self, node, pat: str, remainder) -> list:
        matches = []
        for child in self.get_children(node):
            name = self.get_attribute(child)
            try:
                if self.__match(name, pat):
                    if remainder:
                        matches += self._glob(child, remainder)
                    else:
                        matches.append(child)
            except ResolverError:
                if not self.is_wildcard(pat):
                    raise
        return matches

    @staticmethod
    def is_wildcard(path: str) -> bool:
        """Return `True` is a wildcard."""
        return "?" in path or "*" in path

    def __match(self, name: str, pat: str) -> bool:
        k = (pat, self.ignore_case)
        try:
            re_pat = self._match_cache[k]
        except KeyError:
            res = self.__translate(pat)
            if len(self._match_cache) >= _MAXCACHE:
                self._match_cache.clear()
            flags = 0
            if self.ignore_case:
                flags |= re.IGNORECASE
            self._match_cache[k] = re_pat = re.compile(res, flags=flags)
        return re_pat.match(name) is not None

    def __cmp(self, name, pat):
        return name.upper() == pat.upper() if self.ignore_case else name == pat

    @staticmethod
    def __translate(pat: str) -> str:
        re_pat = ""
        for char in pat:
            if char == "*":
                re_pat += ".*"
            elif char == "?":
                re_pat += "."
            else:
                re_pat += re.escape(char)
        return f"(?ms){re_pat}" + r"\Z"


class ResolverError(RuntimeError):
    def __init__(self, node, child, msg):
        """Resolve Error at `node` handling `child`."""
        super().__init__(msg)
        self.node = node
        self.child = child


class RootResolverError(ResolverError):
    def __init__(self, root):
        """Root Resolve Error, cannot go above root node."""
        msg = f"Cannot go above root node {root!r}"
        super().__init__(root, None, msg)


class ChildResolverError(ResolverError):
    def __init__(self, node, child, names):
        """Child Resolve Error at `node` handling `child`."""
        msg = "{!r} has no child {}. Children are: {}.".format(
            node,
            child,
            ", ".join(names),
        )
        super().__init__(node, child, msg)


class NodeResolver(BaseResolver):
    def __init__(self, path_attr: str = "obj", ignore_case: bool = False):
        """Resolve any `Node` paths using attribute `path_attr`.

        Arguments:
            path_attr: Name of the node attribute to be used for resolving
            ignore_case: Enable case insensisitve handling.
        """
        super().__init__(ignore_case=ignore_case)
        self.path_attr = path_attr

    def get_parent(self, node):
        return node.parent

    def get_children(self, node):
        return node.children

    def get_root(self, node):
        return node.root

    def get_attribute(self, node):
        return getattr(node, self.path_attr)


class MkNodeResolver(NodeResolver):
    def __init__(self, ignore_case: bool = False):
        super().__init__(path_attr="", ignore_case=ignore_case)

    def get_attribute(self, node):
        import mknodes

        match node:
            case mknodes.MkNav():
                return node.section
            case mknodes.MkPage():
                return node.path
            case _:
                return type(node).__name__


if __name__ == "__main__":
    from mknodes import manual, project

    proj = project.Project.for_mknodes()
    root = manual.build(proj)
    resolver = MkNodeResolver()
    result = resolver.glob("*/*/MkAdm*", root)
