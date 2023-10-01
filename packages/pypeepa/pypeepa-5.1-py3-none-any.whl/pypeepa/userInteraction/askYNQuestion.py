import re


def askYNQuestion(message):
    invalid_input = True
    return_val = False
    while invalid_input:
        user_input = input(f"{message} ")
        if bool(re.match(r"[YyNn]", user_input)):
            if bool(re.match(r"[Yy]", user_input)):
                return_val = True
                invalid_input = False
            elif bool(re.match(r"[Nn]", user_input)):
                return_val = False
                invalid_input = False
        else:
            print("\x1B[31mInvalid input! Please input either\x1B[37m y/n")
    return return_val
