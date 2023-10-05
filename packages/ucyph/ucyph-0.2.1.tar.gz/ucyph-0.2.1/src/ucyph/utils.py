import os


def read_file(filename: str) -> str:
    """
    Read the contents of a file

    :param filename: The name of the file to read
    :return: The contents of the file
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"The file \'{filename}\' was not found.")

    with open(filename, 'r') as f:
        s = f.read()
    return s


def write_file(s, output_file) -> None:
    """
    Write the contents of a file

    :param s: The contents of the file
    :param output_file: The name of the file to write
    :return: None
    """
    with open(output_file, 'w') as f:
        f.write(s)
    return None
