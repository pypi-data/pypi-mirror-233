# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-10-01 14:47:47
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Print methods.
"""


from typing import Any, Literal, Optional
from pprint import pformat as pprint_pformat

from .rbase import get_first_notnull, get_name
from .roption import ROption
from .rtext import split_str, fill_width


__all__ = (
    "print_add_frame",
    "rprint"
)


def print_add_frame(
    *contents: Any,
    title: Optional[str],
    width: int,
    frame: Literal["full", "half", "plain"]
) -> None:
    """
    `Print` contents and frame.

    Parameters
    ----------
    contents : Print contents.
    title : Print frame title.
        - `None` : No title.
        - `str` : Use this value as the title.

    width : Print frame width.
    frame : Frame type.
        - `Literal[`full`]` : Build with symbol `═╡╞─║╟╢╔╗╚╝`, and content not can exceed the frame.
            When throw `exception`, then frame is `half` type.
        - `Literal[`half`]` : Build with symbol `═╡╞─`, and content can exceed the frame.
        - `Literal[`plain`]` : Build with symbol `=|-`, and content can exceed the frame.
    """

    # Handle parameter.
    if title is None or len(title) > width - 6:
        title = ""

    # Generate frame.

    ## Full type.
    if frame == "full":
        if title != "":
            title = f"╡ {title} ╞"
        width_in = width - 2
        _contents = []
        try:
            for content in contents:
                content_str = str(content)
                pieces_str = content_str.split("\n")
                content_str = [
                    "║%s║" % fill_width(line_str, " ", width_in)
                    for piece_str in pieces_str
                    for line_str in split_str(piece_str, width_in, True)
                ]
                content = "\n".join(content_str)
                _contents.append(content)
        except:
            frame_top = fill_width(title, "═", width, "center")
            frame_split = "─" * width
            frame_bottom = "═" * width
            _contents = contents
        else:
            frame_top = "╔%s╗" % fill_width(title, "═", width_in, "center")
            frame_split = "╟%s╢" % ("─" * width_in)
            frame_bottom = "╚%s╝" % ("═" * width_in)

    ## Half type.
    elif frame == "half":
        if title != "":
            title = f"╡ {title} ╞"
        frame_top = fill_width(title, "═", width, "center")
        frame_split = "─" * width
        frame_bottom = "═" * width
        _contents = contents

    ## Plain type.
    elif frame == "plain":
        if title != "":
            title = f"| {title} |"
        frame_top = fill_width(title, "=", width, "center")
        frame_split = "-" * width
        frame_bottom = "=" * width
        _contents = contents

    # Print.
    print(frame_top)
    for index, content in enumerate(_contents):
        if index != 0:
            print(frame_split)
        print(content)
    print(frame_bottom)


def rprint(
    *contents: Any,
    title: Optional[str] = None,
    width: Optional[int] = None,
    frame: Optional[Literal["full", "half", "plain"]] = "full",
    format: bool = True
) -> None:
    """
    `Print` formatted contents.

    Parameters
    ----------
    contents : Print contents.
    title : Print frame title.
        - `None` : No title.
        - `str` : Use this value as the title.

    width : Print frame width.
        - `None` : Use attribute `print_width` of object `ROption`.
        - `int` : Use this value.

    frame : Frame type.
        - `Literal[`full`]` : Use attribute `print_frame_full` of object `ROption`.
            Build with symbol `═╡╞─║╟╢╔╗╚╝`, and content not can exceed the frame.
            When throw `exception`, then frame is `half` type.
        - `Literal[`half`]` : Use attribute `print_frame_half` of object `ROption`.
            Build with symbol `═╡╞─`, and content can exceed the frame.
        - `Literal[`plain`]` : Use attribute `print_frame_plain` of object `ROption`.
            Build with symbol `=|-`, and content can exceed the frame.
    
    format : Whether format data of type list or tuple or dict or set.
    """

    # Get parameter by priority.
    width = get_first_notnull(width, ROption.print_width, default="exception")

    # Handle parameter.
    if title is None:
        titles = get_name(contents)
        if titles is not None:
            titles = [title if title[:1] != "`" else "" for title in titles]
            if set(titles) != {""}:
                title = " │ ".join(titles)
    if frame == "full":
        frame = ROption.print_frame_full
    elif frame == "half":
        frame = ROption.print_frame_half
    elif frame == "plain":
        frame = ROption.print_frame_plain

    # Clean.
    if frame == "full":
        _width = width - 2
    else:
        _width = width
    contents_clean = []
    for content in contents:

        ## Replace tab.
        if content.__class__ == str:
            content = content.replace("\t", "    ")

        ## Format contents.
        elif (
            format
            and content.__class__ in (list, tuple, dict, set)
        ):
            content = pprint_pformat(content, width=_width, sort_dicts=False)

        contents_clean.append(content)

    # Print.
    print_add_frame(*contents_clean, title=title, width=width, frame=frame)