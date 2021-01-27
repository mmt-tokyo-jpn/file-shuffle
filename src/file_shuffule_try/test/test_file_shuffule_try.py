from file_shuffule_try.file_shuffule_try import remove_prefix, create_file_names
import pytest
import os
import shutil
import glob


def test_shuffle_two_files() -> None:
    result_file_names = create_file_names(["name1.txt", "name2"], [1, 2])

    assert set(result_file_names) == {("1-name1.txt", "name1.txt"), ("2-name2", "name2")}


def test_shuffle_10_files() -> None:
    files = ["name" + str(i + 1) for i in range(10)]

    numbers = range(1, len(files) + 1)
    result_file_names = list(create_file_names(files, numbers))

    assert any(new_file == "01-name1" for new_file, org_file in result_file_names)
    assert any(new_file == "03-name3" for new_file, org_file in result_file_names)


def test_shuffle_10_files_reshuffle() -> None:
    num_files = 10
    files = [str(num_files - i).zfill(2) + "-" + "name" + str(i + 1) for i in range(num_files)]
    assert "10-name1" in files
    assert "08-name3" in files

    numbers = range(1, len(files) + 1)
    result_file_names = list(create_file_names(files, numbers))

    assert any(new_file == "01-name1" for new_file, org_file in result_file_names)
    assert any(new_file == "03-name3" for new_file, org_file in result_file_names)


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

        # Create an empty file
        files_to_create = ["test_file1.txt", "test_file2.txt"]
        for s in files_to_create:
            open(s, "a").close()

        folder_path = "."
        glob_path = os.path.join(folder_path, "*")
        files_in_folder1 = list(glob.glob(glob_path))

        file_name_tuples = create_file_names(files_in_folder1, range(1, len(files_in_folder1) + 1))
        for new_file_name, orig_file_name in file_name_tuples:
            os.rename(orig_file_name, new_file_name)

        files_in_folder2 = list(glob.glob("./*"))

        assert any("1-test_file1.txt" in s for s in files_in_folder2)

    finally:
        print(folder_to_return)
        os.chdir(folder_to_return)
        shutil.rmtree(test_folder_path, ignore_errors=True)
