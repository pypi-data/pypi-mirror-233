import os.path
from typing import Set, Optional

from .fictusexception import FictusException
from .fictusnode import File, Folder, Node

DEFAULT_ROOT_NAME = "\\"


class FictusFileSystem:
    """
    A FictusFileSystem (FFS) simulates the creation and traversal of a file system.
    The FFS allows for the creation and removal of files and folders,
    """

    def __init__(self, name=DEFAULT_ROOT_NAME) -> None:
        self._root: Folder = Folder(name.strip(""), None)
        self._current: Folder = self._root

    def root(self) -> Folder:
        return self._root

    def current(self) -> Folder:
        return self._current

    @staticmethod
    def _normalize(path: str) -> str:
        return os.path.normpath(path.replace(DEFAULT_ROOT_NAME, "/"))

    def mkdir(self, path: str) -> None:
        """Takes a string of a normalized relative to cwd and adds the directories
        one at a time."""
        if not path:
            raise FictusException("A Folder must contain a non-empty string.")

        # hold onto the current directory
        current = self._current

        normalized_path = self._normalize(path)
        if normalized_path.startswith(os.sep):
            self._to_root()

        folders = {d.value: d for d in self._current.children}

        for part in normalized_path.split(os.sep):
            if not part:
                continue

            if part not in folders:
                folders[part] = Folder(part, self._current)
                self._current.children.append(folders[part])

            self.cd(folders[part].value)
            folders = {d.value: d for d in self._current.children}

        # return to starting directory
        self._current = current

    def mkfile(self, *files: str) -> None:
        """Takes one or more filenames and adds them to the cwd."""
        visited: Set[str] = {
            f.value for f in self._current.children if isinstance(f, File)
        }
        for file in files:
            if not file:
                raise FictusException("A File must contain a non-empty string.")

            if file not in visited:
                visited.add(file)
                self._current.children.append(File(file, self._current))

    def rename(self, old: str, new: str) -> None:
        """Renames a File or Folder based on its name."""
        for content in self._current.children:
            if content.value == old:
                content.value = new
                break

    def cwd(self) -> str:
        """Prints the current working directory."""
        r = []

        node: Optional[Node] = self._current
        while node is not None:
            r.append(node.value)
            node = node.parent

        if r:
            r[-1] = r[-1] + ":"
        return f"{os.sep}".join(reversed(r))

    def _to_root(self) -> None:
        self._current = self._root

    def cd(self, path: str) -> None:
        """Takes a string of a normalized relative to cwd and changes the current"""
        # Return to the current dir if something goes wrong
        current = self._current

        normalized_path = self._normalize(path)
        if normalized_path.startswith(os.sep):
            self._to_root()

        for index, part in enumerate(normalized_path.split(os.sep)):
            if not part:
                continue

            if index == 0 and part.endswith(":"):
                # explicitly saying it's a root name
                temp_part = part.rstrip(":")
                if temp_part == self._root.value:
                    self._to_root()
                    continue

            if part == "..":
                # looking at the parent here, so ensure its valid.
                parent = self._current.parent
                self._current = parent if parent is not None else self._current

            else:
                hm = {
                    f.value: f for f in self._current.children if isinstance(f, Folder)
                }
                if part not in hm:
                    self._current = current
                    raise FictusException(
                        f"Could not path to {normalized_path} from {self.cwd()}."
                    )
                self._current = hm[part]

        return None
