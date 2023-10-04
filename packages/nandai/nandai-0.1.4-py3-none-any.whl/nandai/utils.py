from __future__ import annotations

import asyncio
from tqdm import tqdm
from typing import Callable
from typing import Any


async def batch_async(data: list[Any], async_func: Callable, batch_size: int):
    res = []
    with tqdm(total=len(data)) as pbar:
        for i in range(0, len(data), batch_size):
            batch = data[i:i+batch_size]
            tasks = [async_func(d) for d in batch]
            res += await asyncio.gather(*tasks)
            pbar.update(len(batch))

    return res
