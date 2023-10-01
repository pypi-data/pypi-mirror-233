def convert_to_list(string: str) -> list[str]:
    return [item for item in string]


def check(string: str, *alphabets) -> bool:
    for alphabet in alphabets:
        if string in alphabet:
            return True

    return False
