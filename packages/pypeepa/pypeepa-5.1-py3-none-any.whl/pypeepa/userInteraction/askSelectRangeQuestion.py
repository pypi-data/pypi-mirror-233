from typing import Optional, List
from pypeepa.checks.checkInputIsInt import checkInputIsInt
from pypeepa.userInteraction.askYNQuestion import askYNQuestion


def askSelectRangeQuestion(
    question: str, min: int, max: int, null_possible: Optional[bool] = False
) -> int | List[int] | None:
    """
    Asks the user to select a range of values between min and max\n
    @param: `question`: The question to ask the user.\n
    @param: `min`: The min value\n
    @param: `max`: The max value\n
    @param: `null_posibble`: (Optional) If set to True, users can input empty string instead of the options.\n
    @return: The selected option as int, or if null_possible is set to True, then can also return None.
    """
    invalid_input = True
    while invalid_input:
        user_input = input(
            f"{question} \nTo select a range use '-'.\nTo select multiple use ','.\n eg:- 1,2,3-5,6 \n(select between {min}-{max}):"
        )
        return_value = None
        if user_input == "" and null_possible:
            invalid_input = False
        elif checkInputIsInt(user_input):
            if min <= int(user_input) <= max:
                invalid_input = False
                return_value = int(user_input)
        elif not checkInputIsInt(user_input):
            array_input = user_input.split(",")
            array_input = expandRangeElements(array_input)
            array_input = convertStrToInt(array_input)
            array_input = checkRangeInList(array_input, min, max)
            print("Selected: ", array_input)
            confirm = askYNQuestion("Confirm selection?")
            if confirm:
                return_value = array_input
                invalid_input = False
        else:
            print(f"\x1B[31mInvalid input! Please input within\x1B[37m {min}-{max}")
    return return_value


def checkRangeInList(lst, min, max):
    checked_list = []
    for x in lst:
        if min <= x <= max:
            checked_list.append(x)
        else:
            print("Found element out of range: ", x)
    return checked_list


def convertStrToInt(lst):
    converted_list = []

    for x in lst:
        try:
            if isinstance(x, str) and x.isdigit():
                converted_list.append(int(x))
        except ValueError:
            print("Value Error on:", x)
            pass

    return converted_list


def expandRangeElements(array):
    expanded_array = []

    for element in array:
        try:
            if "-" in str(element):
                start, end = map(int, element.split("-"))
                expanded_array.extend(map(str, range(start, end + 1)))
            else:
                expanded_array.append(str(element))
        except ValueError:
            print("Value Error on:", element)
            pass
    return expanded_array
