import os
import subprocess


def test_encode_caesar_cipher():
    result = subprocess.run(['python3', '-m', 'src.ucyph.ucyph', '3', 'tests/test_files/test_input.txt', '-e', '-k', 'key', '-o', 'tests/test_files/test_output.txt'],
                            capture_output=True, text=True)

    assert result.stdout == 'The encrypted text has been saved to "tests/test_files/test_output.txt"\n'
    with open('tests/test_files/test_output.txt', 'r') as f:
        file_contents = f.read()
    assert file_contents == 'khoor'
    os.remove('tests/test_files/test_output.txt')
