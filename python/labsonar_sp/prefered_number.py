import math

magnitude_prefix = ["y", "z", "a", "f", "p", "n", "μ", "m", "", "k", "M", "G", "T", "P", "E", "Z", "Y"]
magnitude_prefix_offset = 8

def get_engineering_notation(value, unit):
    if value == 0:
        return get_engineering_notation_with_precision(value, 1, unit)

    exp = math.log10(abs(value))
    index = math.floor(exp / 3.0)
    base = value / math.pow(10, index * 3)

    return get_engineering_notation_with_precision(value, 2 - int(math.floor(math.log10(abs(base)))), unit)


def get_engineering_notation_with_precision(value, precision, unit):
    if value == 0:
        if unit != "":
            return "0 " + unit
        return "0"

    exp = math.log10(abs(value))
    index = math.floor(exp / 3.0)
    base = value / math.pow(10, index * 3)

    string = ""

    if precision == 0:
        string = "{:3.0f}"
    elif precision == 1:
        string = "{:3.1f}"
    elif precision == 2:
        string = "{:3.2f}"
    elif precision == 3:
        string = "{:3.3f}"
    elif precision == 4:
        string = "{:3.4f}"
    elif precision == 5:
        string = "{:3.5f}"
    elif precision == 6:
        string = "{:3.6f}"
    elif precision == 7:
        string = "{:3.7f}"
    elif precision == 8:
        string = "{:3.8f}"
    elif precision == 9:
        string = "{:3.9f}"
    else:
        index = len(magnitude_prefix)
    index += magnitude_prefix_offset

    if index < 0 or index >= len(magnitude_prefix):
        string = "{:.05e}"
        index = magnitude_prefix_offset
        base = value

    str = string.format(base)

    if unit == "" and magnitude_prefix[index] == "":
        return str

    return str + " " + magnitude_prefix[index] + unit
