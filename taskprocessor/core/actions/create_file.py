from pathlib import Path
import os

def create(file_path, file_name):

    created = None
    try:
        path = Path(file_path) / file_name
        path.touch()
        created = path
    except Exception as ex:
        print(ex) #TODO: logging and reraising

    return created

if __name__ == '__main__':
    print("Current Working Directory = " + os.getcwd())
    create(os.getcwd(), 'test')
