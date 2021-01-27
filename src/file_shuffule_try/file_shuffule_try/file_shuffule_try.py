import os
import re
from math import log10
from typing import Iterable


def fib(n: int) -> int:
    if n < 2:
        return n
    else:
        return fib(n - 1) + fib(n - 2)


def remove_prefix(input_str: str) -> str:
    result = re.sub(r"^\d+-", "", input_str)
    return result


def create_file_names(files: Iterable[str], numbers: Iterable[int]) -> Iterable[str]:
    inputs = list(zip(files, numbers))

    num_inputs = len(inputs)
    if num_inputs == 0:  # no elements.
        return

    num_letters = int(log10(num_inputs) + 1)

    for file_path, number in inputs:
        split_file_path = os.path.split(file_path)
        file = split_file_path[-1]
        dir_name = os.path.dirname(file_path)
        file_wo_prefix = remove_prefix(file)
        new_filename = str(number).zfill(num_letters) + "-" + file_wo_prefix
        new_path = os.path.join(dir_name, new_filename)
        yield new_path, file

