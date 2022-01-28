from __future__ import annotations

import io
import os
import tempfile

from pathlib import Path


def get_name_from_path(path: str | Path) -> str:
    return Path(path).name


def get_name_from_label(label: str) -> str:
    return label.lower().replace(" ", "_")


def get_extension(path: str | Path) -> str:
    return Path(path).suffix


def get_absolute_path(relative_path: str | Path, cwd: str | Path | None = None) -> str:
    if cwd is None:
        return str(Path(relative_path).absolute())
    else:
        if Path(cwd).is_file():
            return Path(cwd).parent / relative_path
        else:
            return Path(cwd) / relative_path


def list_files(path: str | Path, recursive: bool = True, extensions: list[str] | None = None) -> list[str]:
    # Convert to Path object
    path = Path(path)

    # clean extensions
    if extensions is not None:
        for i in range(len(extensions)):
            if extensions[i].startswith('.'):
                extensions[i] = extensions[i][1:]

    # Check if already a file
    if path.is_file():
        # Check if the file has given extension or else return None
        if extensions is not None and path.suffix.lower() in extensions:
            return [str(path.absolute())]
        else:
            return []

    # find files of given extension
    found_files = []

    if extensions is None:
        if recursive:
            for p in path.rglob('*.*'):
                found_files.append(str(p.absolute()))
        else:
            for p in path.glob('*.*'):
                found_files.append(str(p.absolute()))
    else:
        for e in extensions:
            if recursive:
                for p in path.rglob('*.{}'.format(e)):
                    found_files.append(str(p.absolute()))
            else:
                for p in path.glob('*.{}'.format(e)):
                    found_files.append(str(p.absolute()))

    return found_files


def read_file(path: str | Path) -> str:
    path = Path(path)
    contents = ""
    if path.exists():
        contents = path.read_text() or ""
    return contents


def get_temp_file(file_contents: str, name: str | None = None, extension: str = ".txt"):
    if not extension.startswith('.'):
        extension = '.' + extension

    file = tempfile.NamedTemporaryFile(prefix=name, suffix=extension, delete=False)
    # file = tempfile.NamedTemporaryFile(prefix=name, suffix=extension)
    file.write(file_contents.encode('utf-8'))
    file.seek(0)
    return file


def delete_temp_file(file: io.TextIOWrapper) -> bool:
    file.close()
    os.unlink(file.name)
    return not os.path.exists(file.name)
