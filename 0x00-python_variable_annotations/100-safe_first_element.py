#!/usr/bin/env python3
"""100-safe_first_element"""
from typing import Any, Sequence, Union


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """safe_first_element is return else None"""
    if lst:
        return lst[0]
    else:
        return None
