def countTotalRows(file_path: str):
    """
    Count the total number of rows in a text based file like csv, json, txt etc.
    @param:`file_path`:The path to the file you want to count the total rows in.
    @return:
       The total line count
    """
    with open(file_path, "r") as file:
        line_count = sum(1 for line in file)
    return line_count
