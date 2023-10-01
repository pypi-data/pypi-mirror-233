from __future__ import annotations

import os
import pathlib

from mknodes.utils import downloadhelpers, helpers, superdict


class ConfigFile(superdict.SuperDict):
    def __init__(self, path: str | os.PathLike | None = None):
        super().__init__()
        self.path = path
        if self.path is None:
            return
        self.path = str(path)
        if helpers.is_url(self.path):
            content = downloadhelpers.download(self.path)
            self.load_config(content.decode())
        else:
            self.load_file(self.path)

    def __repr__(self):
        return f"{type(self).__name__}({self.path!r})"

    def __bool__(self):
        return bool(self._data or self.path)

    def get_section_text(
        self,
        *sections: str,
        keep_path: bool = False,
    ) -> str:
        """Try to get data from given path as text.

        If Key path does not exist, return empty string.

        Arguments:
            sections: Sections to dig into
            keep_path: Return result with original nesting
        """
        if not sections:
            raise ValueError(sections)
        section = self.get_section(*sections, keep_path=keep_path)
        return "" if section is None else self._dump(section)

    def load_config(self, data: str):
        """Load a string with loader of given file type.

        Arguments:
            data: String with markup of type as config file
        """
        self._data = self._load(data)

    def dump_config(self) -> str:
        """Dump to string with dumper of given file type."""
        return self._dump(self._data)

    def load_file(self, path: str | os.PathLike):
        """Load a file with loader of given file type.

        Arguments:
            path: Path to the config file
        """
        text = pathlib.Path(path).read_text(encoding="utf-8")
        self.load_config(text)

    @classmethod
    def _dump(cls, data: dict) -> str:
        """Needs to be reimplemented by subclasses."""
        raise NotImplementedError

    @classmethod
    def _load(cls, data: str) -> dict | list:
        """Needs to be reimplemented by subclasses."""
        raise NotImplementedError


if __name__ == "__main__":
    from mknodes.info import tomlfile

    info = tomlfile.TomlFile("pyproject.toml")
    text = info.get_section_text("tool", "hatch", keep_path=True)
    print(text)
