from file_shuffule_try.file_shuffule_try import fib
from typing import Iterable
from math import log10
import pytest
import re
import os
import shutil
import glob


def remove_prefix(input_str: str) -> str:
    result = re.sub(r"^\d+-", "", input_str)
    return result


def create_file_names(files: Iterable[str], numbers: Iterable[int]) -> Iterable[str]:
    inputs = list(zip(files, numbers))

    num_inputs = len(inputs)
    num_letters = int(log10(num_inputs) + 1)

    for file, number in inputs:
        file_wo_prefix = remove_prefix(file)
        yield str(number).zfill(num_letters) + "-" + file_wo_prefix


def test_shuffle_one_file() -> None:
    result_file_names = create_file_names(["name"], [1])

    assert list(result_file_names) == ["1-name"]


def test_shuffle_two_files() -> None:
    result_file_names = create_file_names(["name1", "name2"], [1, 2])

    assert set(result_file_names) == {"1-name1", "2-name2"}


def test_shuffle_10_files() -> None:
    files = ["name" + str(i + 1) for i in range(10)]

    numbers = range(1, len(files) + 1)
    result_file_names = list(create_file_names(files, numbers))

    assert "01-name1" in result_file_names
    assert "03-name3" in result_file_names


def test_shuffle_10_files_reshuffle() -> None:
    files = [str(i + 1).zfill(2) + "-" + "name" + str(i + 1) for i in range(10)]

    numbers = range(1, len(files) + 1)
    result_file_names = list(create_file_names(files, numbers))

    assert "01-name1" in result_file_names
    assert "03-name3" in result_file_names


remove_prefix_test_data = [
    ("02-file_name", "file_name"),
    ("002-my_file", "my_file"),
    ("my_002-file", "my_002-file"),
    ("no_prefix_file", "no_prefix_file"),
]


@pytest.mark.parametrize("input_str, expected", remove_prefix_test_data)
def test_remove_prefix_parameterized(input_str: str, expected: str) -> None:
    result = remove_prefix(input_str)

    assert result == expected


def test_add_prefix_to_the_real_file():
    test_folder = "test_folder"
    assert not os.path.exists(test_folder)

    folder_to_return = os.getcwd()
    test_folder_path = os.path.join(folder_to_return, test_folder)

    try:
        os.mkdir(test_folder_path)
        os.chdir(test_folder_path)
        print(os.getcwd())

        open("test_file1.txt", "a").close()

        result_filenames = create_file_names(["test_file1.txt"], [1])

        os.rename("test_file1.txt", list(result_filenames)[0])

        files_in_folder = list(glob.glob("./*"))

        assert any("1-test_file1.txt" in s for s in files_in_folder)

        for n in files_in_folder:
            print(n)


    finally:
        print(folder_to_return)
        os.chdir(folder_to_return)
        shutil.rmtree(test_folder_path, ignore_errors=True)
