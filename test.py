from __future__ import annotations

from time import time

import anyio
import psycopg


async def main() -> None:
    async def hog(dsn: str, durations: list[float]):
        start = time()
        async with await psycopg.AsyncConnection.connect(dsn) as aconn:
            await aconn.execute('SELECT pg_sleep(10)')
        end = time()
        durations.append(end - start)

    for dsn in (
        # connect to cloudsql via pgbouncer + proxy
        'postgres://postgres:postgres@127.0.0.1:5432/proxy',
        # connect to cloudsql via pgbouncer + direct
        'postgres://postgres:postgres@127.0.0.1:5432/direct',
        # connect to cloudsql direct (change IP to be private or public iP)
        'postgres://postgres:postgres@35.238.106.212/postgres',
    ):
        durations: list[float] = []
        async with anyio.create_task_group() as tg:
            for _ in range(32):
                tg.start_soon(hog, dsn, durations)
        x = [f'{d:.2f}s' for d in durations]
        print(f'{dsn}:\n{x}\n\n')

anyio.run(main)
