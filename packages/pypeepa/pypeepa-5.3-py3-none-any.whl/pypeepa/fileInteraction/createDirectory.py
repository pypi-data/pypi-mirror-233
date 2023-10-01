import os


def createDirectory(directory_path: str) -> None:
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
