#!/usr/bin/env python3
"""2-measure_runtime"""

import asyncio
import time

async_comprehension = __import__('1-async_comprehension').async_comprehension

async def measure_runtime()-> float:
    """hould measure the total runtime and return it."""
    s = time.perf_counter()
    await async_comprehension()
    return time.perf_counter() - s
