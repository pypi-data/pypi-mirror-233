#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

qrstu.__main__

python3 -m qrstu command line script


Copyright (C) 2023 Rainer Schwarzbach

This file is part of qrstu.

qrstu is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

qrstu is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""


import sys

from qrstu import commandline


#
# Functions
#


def main(*args: str) -> int:
    """Execute the main program

    :param args: the command line arguments
    :returns: the script returncode
    """
    program = commandline.Program(*args)
    return program.execute()


if __name__ == "__main__":
    sys.exit(main())  # NOT TESTABLE


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
