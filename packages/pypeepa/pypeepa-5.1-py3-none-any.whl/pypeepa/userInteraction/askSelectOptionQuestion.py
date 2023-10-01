from typing import Optional
from pypeepa.checks.checkInputIsInt import checkInputIsInt


def askSelectOptionQuestion(
    question: str, min: int, max: int, null_possible: Optional[bool] = False
) -> int | None:
    """
    Asks the user to select between a range of values set between min and max\n
    @param: `question`: The question to ask the user.\n
    @param: `min`: The min value\n
    @param: `max`: The max value\n
    @param: `null_posibble`: (Optional) If set to True, users can input empty string instead of the options.\n
    @return: The selected option as int, or if null_possible is set to True, then can also return None.
    """
    invalid_input = True
    while invalid_input:
        user_input = input(f"{question} (select between {min}-{max}):")
        return_value = None
        if user_input == "" and null_possible:
            invalid_input = False
        elif checkInputIsInt(user_input):
            if min <= int(user_input) <= max:
                invalid_input = False
                return_value = int(user_input)
        else:
            print(f"\x1B[31mInvalid input! Please input within\x1B[37m {min}-{max}")
    return return_value
