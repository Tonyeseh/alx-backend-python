#!/usr/bin/env python3
"""4-tasks"""

import asyncio
from typing import List

task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """spawn wait_random n times with the specified max_delay.

    return the list of all the delays (float values)."""
    wait_lst = await asyncio.gather(*(task_wait_random(max_delay) for i in range(n)))

    return sorted(wait_lst)
