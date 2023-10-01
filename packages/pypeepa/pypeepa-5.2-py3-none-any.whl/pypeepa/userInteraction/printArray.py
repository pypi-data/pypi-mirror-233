from typing import List


def printArray(array: List) -> None:
    for index, value in enumerate(array):
        print(f"[{index+1}]: {value}")
