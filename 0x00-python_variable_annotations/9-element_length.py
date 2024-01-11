#!/usr/bin/env python3
"""9-element_length"""
from typing import Iterable, List, Sequence, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """returns a list with the iterable and it's lenght as tuple as elements"""
    return [(i, len(i)) for i in lst]
