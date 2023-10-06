import textwrap


def message(text: str, max_line_length: int = 60) -> str:
    """
    Splits a text so it fits into the maximum line length and formats it
    for showing in the screen.
    """

    # message = "\n\t> "
    # middle_space = ""
    # for word in text.split(" "):
    #     message = message + middle_space + word
    #     if len(message) >= max_line_length:
    #         message = message + "\n\t "

    #     middle_space = " "

    # return message.removesuffix("\t ")

    lines = textwrap.wrap(text, max_line_length, break_long_words=False)

    return "\n\t> " + "\n\t  ".join(lines) + "\n"
