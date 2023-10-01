"""
This is a modified main file, so might not run as application.

Converts the Unicode text file into a python dictionary.
Was run from the project root.
"""
import os
import sys

sys.path[0] = os.path.dirname(sys.path[0])


from celestine import load
from celestine.file import (
    module_save,
    text_load,
)


def work(document):
    for line in document:
        strip = line.strip()
        split = strip.split(";")

        number = split[0]
        number = int(number, 16)

        name = split[1]
        if name == "<control>":
            name = split[10]
            if name == "":
                # U+0099
                name = "Single Graphic Character Introducer"

        elif name[0] == "<":
            continue

        name = name.split("(")[0]
        name = name.strip()

        name = name.replace(" ", "_")
        name = name.replace("-", "_")

        text = f"{name} = chr({number})\n"

        yield text


file = load.pathwayway("UnicodeData.txt")

def read_stream(lines: GE[S, N, N]) -> S:
    string = io.StringIO()
    for line in lines:
        string.write(line)

    value = string.getvalue()
    return value

with text_load(file) as lines:
    load = read_stream(lines)
    text = work(load)
module_save(text, "unicode")
