from pathlib import Path


def run(file_path, file_name):

    created = None
    try:
        path = Path(file_path) / file_name
        path.touch()
        created = path
    except Exception as ex:
        print(ex)  # TODO: logging and reraising

    return created


if __name__ == '__main__':

    run('/home/home/mh/Documents/DEV/ARTFX/TP/tests', 'foo')


