def checkInputIsInt(input: str) -> bool:
    try:
        val = int(input)
        return True
    except ValueError:
        try:
            val = float(input)
            return False
        except ValueError:
            return False
