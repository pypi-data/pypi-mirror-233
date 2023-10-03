"""
Copyright (c) 2023 NotAussie

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""JSPrint - A JavaScript way of printing to the console."""

# Imports
from datetime import datetime  # Built-in

# Version
__version__ = "0.0.3"


# Colours
class Colour:
    def __init__(self):
        pass

    white = "\033[0m"
    red = "\033[31m"
    green = "\033[32m"
    yellow = "\033[33m"
    blue = "\033[34m"
    purple = "\033[35m"
    cyan = "\033[36m"
    grey = "\033[37m"


# Styles
class Styles:
    def __init__(self):
        pass

    default = "\033[0m"
    bold = "\033[1m"
    underline = "\033[4m"
    reversed = "\033[7m"
    reset = "\033[0m"


# Extra
class Extra:
    def __init__(self):
        pass

    @staticmethod
    def date():
        return f"{Colour.grey}[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}]{Styles.reset}"


class JSP:
    def __init__(self):
        pass

    def log(self, message: str):
        print(
            f"{Extra.date()} {Colour.blue}[LOG]{Colour.white} {message}{Styles.reset}"
        )

    def warn(self, message: str):
        print(
            f"{Extra.date()} {Colour.yellow}[WARN]{Colour.white} {message}{Styles.reset}"
        )

    def error(self, message: str):
        print(
            f"{Extra.date()} {Colour.red}[ERROR]{Colour.white} {message}{Styles.reset}"
        )

    def info(self, message: str):
        print(
            f"{Extra.date()} {Colour.blue}[INFO]{Colour.white} {message}{Styles.reset}"
        )

    def success(self, message: str):
        print(
            f"{Extra.date()} {Colour.green}[SUCCESS]{Colour.white} {message}{Styles.reset}"
        )

    def debug(self, message: str):
        print(
            f"{Extra.date()} {Colour.purple}[DEBUG]{Colour.white} {message}{Styles.reset}"
        )

    def trace(self, message: str):
        print(
            f"{Extra.date()} {Colour.grey}[TRACE]{Colour.white} {message}{Styles.reset}"
        )
