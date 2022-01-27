import six
import io
import tempfile

if six.PY2:
    from pathlib2 import Path
else:
    from pathlib import Path


def get_name_from_path(path):
    return Path(path).name


def get_name_from_label(label):
    return label.lower().replace(" ", "_")


def get_extension(path):
    return Path(path).suffix


def get_absolute_path(relative_path, cwd=None):
    if cwd is None:
        return Path(relative_path).absolute()
    else:
        if Path(cwd).is_file():
            return Path(cwd).parent / relative_path
        else:
            return Path(cwd) / relative_path


def list_files(path, recursive=True, extensions=None):
    # Convert to Path object
    path = Path(path)

    # clean extensions
    for i in range(len(extensions)):
        if extensions[i].startswith('.'):
            extensions[i] = extensions[i][1:]

    # Check if already a file
    if path.is_file():
        # Check if the file has given extension or else return None
        if extensions is not None and path.suffix.lower() in extensions:
            return [path.absolute()]
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


def read_file(path):
    f = io.open(path)
    contents = f.read()
    f.close()
    return contents


def get_temp_file(file_contents, name=None, extension="txt"):
    file = tempfile.NamedTemporaryFile(prefix=name, suffix=extension)
    file.write(file_contents)
    file.seek(0)
    return file


def delete_temp_file(file):
    file.close()
