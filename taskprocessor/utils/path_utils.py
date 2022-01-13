import six
import io

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


def list_files(path, recursive=True, extensions=None):
    # clean base path
    if str(path).endswith('/') or str(path).endswith('\\'):
        path = str(path)[:-1]
    # clean extensions
    for i in range(len(extensions)):
        if extensions[i].startswith('.'):
            extensions[i] = extensions[i][1:]

    # find files of given extension
    found_files = []

    if extensions is None:
        if recursive:
            for path in Path(path).rglob('*.*'):
                found_files.append(str(path.absolute()))
        else:
            for path in Path(path).glob('*.*'):
                found_files.append(str(path.absolute()))
    else:
        for e in extensions:
            if recursive:
                for path in Path(path).rglob('*.{}'.format(e)):
                    found_files.append(str(path.absolute()))
            else:
                for path in Path(path).glob('*.{}'.format(e)):
                    found_files.append(str(path.absolute()))

    return found_files


def read_file(path):
    f = io.open(path)
    contents = f.read()
    f.close()
    return contents
