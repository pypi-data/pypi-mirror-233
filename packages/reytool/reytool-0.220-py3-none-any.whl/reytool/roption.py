# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-02-18 19:27:04
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Method options.
"""


from typing import Literal


__all__ = (
    "ROption",
)


class ROption(object):
    """
    Rey's `option` type.
    """

    # Default width of method rprint.
    print_width: int = 100

    # Default frame type of method rprint.
    print_frame_full: Literal["full", "half", "plain"] = "full"
    print_frame_half: Literal["full", "half", "plain"] = "half"
    print_frame_plain: Literal["full", "half", "plain"] = "plain"

    # Default whether report SQL execute information.
    report_execute_info: bool = False