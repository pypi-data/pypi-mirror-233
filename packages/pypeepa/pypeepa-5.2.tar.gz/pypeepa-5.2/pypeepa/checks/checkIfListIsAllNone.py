def checkIfListIsAllNone(array):
    for value in array:
        if value is not None:
            return False  # If any value is not None, return False
    return True
