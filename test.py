from __future__ import annotations

from time import time
from typing import Any

import anyio
import psycopg


async def main() -> None:
    async def hog(dsn: str, durations: list[float]):
        start = time()
        conn = await psycopg.AsyncConnection[Any].connect(dsn)
        await conn.execute('SELECT pg_sleep(10)')
        end = time()
        durations.append(end - start)

    for dsn in (
        # connect to cloudsql via pgbouncer
        'postgres://postgres:postgres@127.0.0.1:5432/cloudsql',
        # connect to postgres via pgbouncer
        'postgres://postgres:postgres@127.0.0.1:5432/local',
        # connect to cloudsql directly
        'postgres://postgres:postgres@127.0.0.1:5434/postgres',
    ):
        durations: list[float] = []
        async with anyio.create_task_group() as tg:
            for _ in range(32):
                tg.start_soon(hog, dsn, durations)
        print(f'{dsn}:\n{[f'{d:.2f}s' for d in durations]}\n\n')

anyio.run(main)
