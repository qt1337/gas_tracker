import json
import os.path


def load_data(path: str):
    """
    loads data from given path
    :param path: path of file to open
    :return: json
    """
    with open(path, 'r') as outfile:
        return_data = json.loads(outfile.read())
    outfile.close()
    return return_data


def create_empty_file(path: str):
    """
    creates empty file
    :param path: path of file to create
    """
    with open(path, 'w') as outfile:
        pass
    outfile.close()


def save_data(path: str, input_data):
    """
    saves data to given path
    :param path: path of file to save
    :param input_data: data which will be saved
    """
    with open(path, 'w') as infile:
        infile.write(json.dumps(input_data, indent=4))
    infile.close()


def check_and_create_dir(path: str):
    """
    creates a directory in given path if it doesn't exist yet
    :param path: path of dir to check/create
    """
    if not os.path.isdir(path):
        os.makedirs(path)


def check_and_create_file_with_return(path: str) -> bool:
    """
    checks if file exists or is empty and creates it
    :param path: path to file to check
    :return: boolean
    """
    file_exists = os.path.isfile(path) and os.stat(path).st_size != 0
    if not file_exists:
        create_empty_file(path)
    return file_exists
