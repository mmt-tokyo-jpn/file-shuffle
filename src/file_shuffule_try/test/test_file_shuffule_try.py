from file_shuffule_try.file_shuffule_try import fib
from typing import Iterable

def test_fib() -> None:
    assert fib(0) == 0
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(3) == 2
    assert fib(4) == 3
    assert fib(5) == 5
    assert fib(10) == 55



def create_file_names(files: Iterable[str], numbers: Iterable[int]) -> Iterable[str]:

    inputs = zip(files, numbers)

    for file, number in inputs:
        yield str(number) + "-" + file



def test_shuffle_one_file() -> None:

    result_file_names = create_file_names(["name"], [1])

    assert list(result_file_names) == ["1-name"]


def test_shuffle_one_file2() -> None:

    result_file_names = create_file_names(["name1", "name2"], [1, 2])

    assert set(result_file_names) == {"1-name1", "2-name2"}

