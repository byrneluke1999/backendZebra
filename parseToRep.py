import json
import re

# function to split string into indivudal streets.


def parse(s):
    # [1|2|3|4|5]
    s = s.split('|')
    street = []
    for h in s:
        street.append(remove_chars(h))
    dictver = convert_d(street)
    return dictver

# removing extra brackets and splittng string of all attribute values into inidvudal values
# From "smo(koo),col(yel)" -> "smo(koo)", "col(yel)"
# removing house indices also.


def remove_chars(s):
    s = s.replace(",", "")
    return ''.join((letter for letter in s if not letter.isdigit()))


def convert_d(street):
    d = {}
    for index, item in enumerate(street):
        item = item.split(")")
        # replacing empty string with '-' for clarity.
        newItems = ["---" if x == '' else x for x in item]
        # ensure houses can only contain 5 variables. bug with additional element "---" when replacing empty.
        if len(newItems) == 6:
            del newItems[-1]
        d[f"House{index+1}"] = newItems
    return d
# returning a dictionary with five keys, the houses and embedded lists with the values of each attribute.
