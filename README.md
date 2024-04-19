# pgbouncer / cloudsqlproxy interaction

This reproduces an issue I've encountered with pgbouncer and the cloudsqlproxy.
Combining them leads to slow connections, but individually they work fine.

## Setup

1. Create a Cloud SQL instance. See [GCP Docs](https://cloud.google.com/sql/docs/postgres/connect-instance-auth-proxy).
2. Create a service account and credential keys. See [GCP Docs](https://cloud.google.com/sql/docs/postgres/connect-auth-proxy?authuser=1#create-service-account).
3. Put the credential keys in the `keys.json` file.
4. Bring up docker-compose.
5. Run `test.py` (after installing `requirements.txt`).

## Observations

For both connecting to postgres via pgbouncer and cloudsqlproxy directly the connection is fast.
If connecting to cloudsqlproxy via pgbouncer connections are very slow.

```
postgres://postgres:postgres@127.0.0.1:5432/cloudsql:
['10.75s', '10.90s', '11.37s', '11.47s', '11.98s', '12.01s', '12.30s', '12.57s', '12.99s', '13.15s', '13.57s', '13.67s', '14.21s', '14.21s', '14.47s', '14.72s', '15.01s', '15.29s', '15.56s', '15.82s', '16.09s', '16.36s', '16.62s', '16.86s', '17.11s', '17.36s', '17.66s', '18.04s', '18.20s', '18.44s', '18.84s', '18.94s']


postgres://postgres:postgres@127.0.0.1:5432/local:
['10.19s', '10.19s', '10.20s', '10.20s', '10.20s', '10.21s', '10.21s', '10.21s', '10.23s', '10.24s', '10.24s', '10.24s', '10.25s', '10.25s', '10.25s', '10.27s', '10.28s', '10.28s', '10.28s', '10.29s', '10.29s', '10.29s', '10.31s', '10.33s', '10.33s', '10.33s', '10.33s', '10.33s', '10.34s', '10.34s', '10.35s', '10.36s']


postgres://postgres:postgres@127.0.0.1:5434/postgres:
['10.15s', '10.17s', '10.17s', '10.17s', '10.17s', '10.17s', '10.17s', '10.17s', '10.17s', '10.17s', '10.17s', '10.17s', '10.17s', '10.17s', '10.17s', '10.17s', '10.17s', '10.17s', '10.17s', '10.17s', '10.18s', '10.17s', '10.17s', '10.17s', '10.17s', '10.18s', '10.17s', '10.18s', '10.17s', '10.17s', '10.17s', '10.17s']
```

There's a lot of logs for the pgbouncer -> cloudsqlproxy case but not for others.

```
cloudql-1    | 2024/04/19 14:20:50 Authorizing with the credentials file at "/key.json"
cloudql-1    | 2024/04/19 14:20:50 [<instance-name>] Listening on [::]:5432
cloudql-1    | 2024/04/19 14:20:50 The proxy has started successfully and is ready for new connections!
cloudql-1    | 2024/04/19 14:20:50 [<instance-name>] Connection info added to cache
cloudql-1    | 2024/04/19 14:20:50 [<instance-name>] Connection info refresh operation started
postgres-1   | The files belonging to this database system will be owned by user "postgres".
postgres-1   | This user must also own the server process.
postgres-1   | 
postgres-1   | The database cluster will be initialized with locale "en_US.utf8".
postgres-1   | The default database encoding has accordingly been set to "UTF8".
postgres-1   | The default text search configuration will be set to "english".
postgres-1   | 
postgres-1   | Data page checksums are disabled.
postgres-1   | 
postgres-1   | fixing permissions on existing directory /var/lib/postgresql/data ... ok
postgres-1   | creating subdirectories ... ok
postgres-1   | selecting dynamic shared memory implementation ... posix
postgres-1   | selecting default max_connections ... 100
postgres-1   | selecting default shared_buffers ... 128MB
postgres-1   | selecting default time zone ... Etc/UTC
postgres-1   | creating configuration files ... ok
pgbouncer-1  | 2024-04-19 14:20:50.573 UTC [1] LOG kernel file descriptor limit: 1048576 (hard: 1048576); max_client_conn: 100, max expected fd use: 312
pgbouncer-1  | 2024-04-19 14:20:50.573 UTC [1] LOG kernel file descriptor limit: 1048576 (hard: 1048576); max_client_conn: 100, max expected fd use: 312
pgbouncer-1  | 2024-04-19 14:20:50.574 UTC [1] LOG listening on 0.0.0.0:5432
pgbouncer-1  | 2024-04-19 14:20:50.574 UTC [1] LOG listening on unix:/tmp/.s.PGSQL.5432
pgbouncer-1  | 2024-04-19 14:20:50.574 UTC [1] LOG process up: PgBouncer 1.22.0, libevent 2.1.12-stable (epoll), adns: evdns2, tls: OpenSSL 3.1.4 24 Oct 2023
pgbouncer-1  | 2024-04-19 14:20:50.574 UTC [1] LOG listening on 0.0.0.0:5432
pgbouncer-1  | 2024-04-19 14:20:50.574 UTC [1] LOG listening on unix:/tmp/.s.PGSQL.5432
pgbouncer-1  | 2024-04-19 14:20:50.574 UTC [1] LOG process up: PgBouncer 1.22.0, libevent 2.1.12-stable (epoll), adns: evdns2, tls: OpenSSL 3.1.4 24 Oct 2023
postgres-1   | running bootstrap script ... ok
postgres-1   | performing post-bootstrap initialization ... ok
postgres-1   | syncing data to disk ... ok
postgres-1   | 
postgres-1   | 
postgres-1   | Success. You can now start the database server using:
postgres-1   | 
postgres-1   |     pg_ctl -D /var/lib/postgresql/data -l logfile start
postgres-1   | 
postgres-1   | initdb: warning: enabling "trust" authentication for local connections
postgres-1   | initdb: hint: You can change this by editing pg_hba.conf or using the option -A, or --auth-local and --auth-host, the next time you run initdb.
postgres-1   | waiting for server to start....2024-04-19 14:20:50.890 UTC [48] LOG:  starting PostgreSQL 15.6 (Debian 15.6-1.pgdg120+2) on aarch64-unknown-linux-gnu, compiled by gcc (Debian 12.2.0-14) 12.2.0, 64-bit
postgres-1   | 2024-04-19 14:20:50.890 UTC [48] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
postgres-1   | 2024-04-19 14:20:50.893 UTC [51] LOG:  database system was shut down at 2024-04-19 14:20:50 UTC
postgres-1   | 2024-04-19 14:20:50.895 UTC [48] LOG:  database system is ready to accept connections
postgres-1   |  done
postgres-1   | server started
cloudql-1    | 2024/04/19 14:20:50 [<instance-name>] Connection info refresh operation complete
cloudql-1    | 2024/04/19 14:20:50 [<instance-name>] Current certificate expiration = 2024-04-19T15:20:50Z
cloudql-1    | 2024/04/19 14:20:50 [<instance-name>] Connection info refresh operation scheduled at 2024-04-19T15:16:50Z (now + 56m0s)
postgres-1   | 
postgres-1   | /usr/local/bin/docker-entrypoint.sh: ignoring /docker-entrypoint-initdb.d/*
postgres-1   | 
postgres-1   | 2024-04-19 14:20:51.001 UTC [48] LOG:  received fast shutdown request
postgres-1   | waiting for server to shut down....2024-04-19 14:20:51.003 UTC [48] LOG:  aborting any active transactions
postgres-1   | 2024-04-19 14:20:51.004 UTC [48] LOG:  background worker "logical replication launcher" (PID 54) exited with exit code 1
postgres-1   | 2024-04-19 14:20:51.004 UTC [49] LOG:  shutting down
postgres-1   | 2024-04-19 14:20:51.005 UTC [49] LOG:  checkpoint starting: shutdown immediate
postgres-1   | 2024-04-19 14:20:51.008 UTC [49] LOG:  checkpoint complete: wrote 3 buffers (0.0%); 0 WAL file(s) added, 0 removed, 0 recycled; write=0.002 s, sync=0.001 s, total=0.005 s; sync files=2, longest=0.001 s, average=0.001 s; distance=0 kB, estimate=0 kB
postgres-1   | 2024-04-19 14:20:51.010 UTC [48] LOG:  database system is shut down
postgres-1   |  done
postgres-1   | server stopped
postgres-1   | 
postgres-1   | PostgreSQL init process complete; ready for start up.
postgres-1   | 
postgres-1   | 2024-04-19 14:20:51.121 UTC [1] LOG:  starting PostgreSQL 15.6 (Debian 15.6-1.pgdg120+2) on aarch64-unknown-linux-gnu, compiled by gcc (Debian 12.2.0-14) 12.2.0, 64-bit
postgres-1   | 2024-04-19 14:20:51.121 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
postgres-1   | 2024-04-19 14:20:51.121 UTC [1] LOG:  listening on IPv6 address "::", port 5432
postgres-1   | 2024-04-19 14:20:51.123 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
postgres-1   | 2024-04-19 14:20:51.125 UTC [62] LOG:  database system was shut down at 2024-04-19 14:20:51 UTC
postgres-1   | 2024-04-19 14:20:51.127 UTC [1] LOG:  database system is ready to accept connections
pgbouncer-1  | 2024-04-19 14:20:55.931 UTC [1] LOG C-0xffff81ec8670: cloudsql/postgres@192.168.65.1:27815 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.931 UTC [1] LOG C-0xffff81ec83c0: cloudsql/postgres@192.168.65.1:27814 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.931 UTC [1] LOG C-0xffff81ec8e80: cloudsql/postgres@192.168.65.1:27818 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.931 UTC [1] LOG C-0xffff81ec8920: cloudsql/postgres@192.168.65.1:27816 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.931 UTC [1] LOG C-0xffff81ec9940: cloudsql/postgres@192.168.65.1:27823 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.931 UTC [1] LOG C-0xffff81ec9690: cloudsql/postgres@192.168.65.1:27820 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.931 UTC [1] LOG C-0xffff81ec8670: cloudsql/postgres@192.168.65.1:27815 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.931 UTC [1] LOG C-0xffff81ec83c0: cloudsql/postgres@192.168.65.1:27814 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.931 UTC [1] LOG C-0xffff81ec8e80: cloudsql/postgres@192.168.65.1:27818 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.931 UTC [1] LOG C-0xffff81ec8920: cloudsql/postgres@192.168.65.1:27816 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.931 UTC [1] LOG C-0xffff81ec9940: cloudsql/postgres@192.168.65.1:27823 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.931 UTC [1] LOG C-0xffff81ec9690: cloudsql/postgres@192.168.65.1:27820 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.931 UTC [1] LOG C-0xffff81ec93e0: cloudsql/postgres@192.168.65.1:27821 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.931 UTC [1] LOG C-0xffff81ec9130: cloudsql/postgres@192.168.65.1:27819 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.931 UTC [1] LOG C-0xffff81eca400: cloudsql/postgres@192.168.65.1:27826 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.931 UTC [1] LOG C-0xffff81ec9ea0: cloudsql/postgres@192.168.65.1:27824 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.931 UTC [1] LOG C-0xffff81eca6b0: cloudsql/postgres@192.168.65.1:27827 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.931 UTC [1] LOG C-0xffff81ec8bd0: cloudsql/postgres@192.168.65.1:27817 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.931 UTC [1] LOG C-0xffff81ecc440: cloudsql/postgres@192.168.65.1:27843 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.931 UTC [1] LOG C-0xffff81ecc190: cloudsql/postgres@192.168.65.1:27841 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.931 UTC [1] LOG C-0xffff81ecbee0: cloudsql/postgres@192.168.65.1:27839 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.931 UTC [1] LOG C-0xffff81ecc9a0: cloudsql/postgres@192.168.65.1:27836 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.931 UTC [1] LOG C-0xffff81eccf00: cloudsql/postgres@192.168.65.1:27840 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.931 UTC [1] LOG C-0xffff81eca150: cloudsql/postgres@192.168.65.1:27825 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.932 UTC [1] LOG C-0xffff81ec9bf0: cloudsql/postgres@192.168.65.1:27822 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.932 UTC [1] LOG C-0xffff81ecb980: cloudsql/postgres@192.168.65.1:27835 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.932 UTC [1] LOG C-0xffff81ecb170: cloudsql/postgres@192.168.65.1:27831 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.932 UTC [1] LOG C-0xffff81ecaec0: cloudsql/postgres@192.168.65.1:27830 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.932 UTC [1] LOG C-0xffff81eca960: cloudsql/postgres@192.168.65.1:27828 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.932 UTC [1] LOG C-0xffff81ecac10: cloudsql/postgres@192.168.65.1:27829 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.932 UTC [1] LOG C-0xffff81ecbc30: cloudsql/postgres@192.168.65.1:27837 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.932 UTC [1] LOG C-0xffff81ecb6d0: cloudsql/postgres@192.168.65.1:27833 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.932 UTC [1] LOG C-0xffff81ecb420: cloudsql/postgres@192.168.65.1:27832 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.932 UTC [1] LOG C-0xffff81eccc50: cloudsql/postgres@192.168.65.1:27838 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.932 UTC [1] LOG C-0xffff81ecd1b0: cloudsql/postgres@192.168.65.1:27842 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.931 UTC [1] LOG C-0xffff81ec93e0: cloudsql/postgres@192.168.65.1:27821 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.931 UTC [1] LOG C-0xffff81ec9130: cloudsql/postgres@192.168.65.1:27819 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.931 UTC [1] LOG C-0xffff81eca400: cloudsql/postgres@192.168.65.1:27826 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.931 UTC [1] LOG C-0xffff81ec9ea0: cloudsql/postgres@192.168.65.1:27824 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.931 UTC [1] LOG C-0xffff81eca6b0: cloudsql/postgres@192.168.65.1:27827 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.931 UTC [1] LOG C-0xffff81ec8bd0: cloudsql/postgres@192.168.65.1:27817 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.931 UTC [1] LOG C-0xffff81ecc440: cloudsql/postgres@192.168.65.1:27843 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.931 UTC [1] LOG C-0xffff81ecc190: cloudsql/postgres@192.168.65.1:27841 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.931 UTC [1] LOG C-0xffff81ecbee0: cloudsql/postgres@192.168.65.1:27839 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.931 UTC [1] LOG C-0xffff81ecc9a0: cloudsql/postgres@192.168.65.1:27836 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.931 UTC [1] LOG C-0xffff81eccf00: cloudsql/postgres@192.168.65.1:27840 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.931 UTC [1] LOG C-0xffff81eca150: cloudsql/postgres@192.168.65.1:27825 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.932 UTC [1] LOG C-0xffff81ec9bf0: cloudsql/postgres@192.168.65.1:27822 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.932 UTC [1] LOG C-0xffff81ecb980: cloudsql/postgres@192.168.65.1:27835 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.932 UTC [1] LOG C-0xffff81ecb170: cloudsql/postgres@192.168.65.1:27831 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.932 UTC [1] LOG C-0xffff81ecaec0: cloudsql/postgres@192.168.65.1:27830 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.932 UTC [1] LOG C-0xffff81eca960: cloudsql/postgres@192.168.65.1:27828 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.932 UTC [1] LOG C-0xffff81ecac10: cloudsql/postgres@192.168.65.1:27829 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.932 UTC [1] LOG C-0xffff81ecbc30: cloudsql/postgres@192.168.65.1:27837 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.932 UTC [1] LOG C-0xffff81ecb6d0: cloudsql/postgres@192.168.65.1:27833 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.932 UTC [1] LOG C-0xffff81ecb420: cloudsql/postgres@192.168.65.1:27832 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.932 UTC [1] LOG C-0xffff81eccc50: cloudsql/postgres@192.168.65.1:27838 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.932 UTC [1] LOG C-0xffff81ecd1b0: cloudsql/postgres@192.168.65.1:27842 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.932 UTC [1] LOG C-0xffff81ecc6f0: cloudsql/postgres@192.168.65.1:27834 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.932 UTC [1] LOG C-0xffff81ecd710: cloudsql/postgres@192.168.65.1:27845 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.932 UTC [1] LOG C-0xffff81ecd460: cloudsql/postgres@192.168.65.1:27844 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.932 UTC [1] LOG C-0xffff81ecc6f0: cloudsql/postgres@192.168.65.1:27834 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.932 UTC [1] LOG C-0xffff81ecd710: cloudsql/postgres@192.168.65.1:27845 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:55.932 UTC [1] LOG C-0xffff81ecd460: cloudsql/postgres@192.168.65.1:27844 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:20:56.064 UTC [1] LOG S-0xffff81e6d3f0: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:56914)
pgbouncer-1  | 2024-04-19 14:20:56.064 UTC [1] LOG S-0xffff81e6d3f0: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:56914)
cloudql-1    | 2024/04/19 14:20:56 [<instance-name>] Accepted connection from 172.24.0.4:56914
cloudql-1    | 2024/04/19 14:20:56 [<instance-name>] Now = 2024-04-19T14:20:56Z, Current cert expiration = 2024-04-19T15:20:50Z
cloudql-1    | 2024/04/19 14:20:56 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:20:56 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:20:56 [<instance-name>] Accepted connection from 172.24.0.4:56918
cloudql-1    | 2024/04/19 14:20:56 [<instance-name>] Now = 2024-04-19T14:20:56Z, Current cert expiration = 2024-04-19T15:20:50Z
pgbouncer-1  | 2024-04-19 14:20:56.379 UTC [1] LOG S-0xffff81e6d6a0: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:56918)
pgbouncer-1  | 2024-04-19 14:20:56.379 UTC [1] LOG S-0xffff81e6d6a0: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:56918)
cloudql-1    | 2024/04/19 14:20:56 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:20:56 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:20:56.670 UTC [1] LOG S-0xffff81e6d950: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:56920)
pgbouncer-1  | 2024-04-19 14:20:56.670 UTC [1] LOG S-0xffff81e6d950: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:56920)
cloudql-1    | 2024/04/19 14:20:56 [<instance-name>] Accepted connection from 172.24.0.4:56920
cloudql-1    | 2024/04/19 14:20:56 [<instance-name>] Now = 2024-04-19T14:20:56Z, Current cert expiration = 2024-04-19T15:20:50Z
cloudql-1    | 2024/04/19 14:20:56 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:20:56 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:20:56.961 UTC [1] LOG S-0xffff81e6dc00: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45440)
pgbouncer-1  | 2024-04-19 14:20:56.961 UTC [1] LOG S-0xffff81e6dc00: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45440)
cloudql-1    | 2024/04/19 14:20:56 [<instance-name>] Accepted connection from 172.24.0.4:45440
cloudql-1    | 2024/04/19 14:20:56 [<instance-name>] Now = 2024-04-19T14:20:56Z, Current cert expiration = 2024-04-19T15:20:50Z
cloudql-1    | 2024/04/19 14:20:56 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:20:56 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:20:57 [<instance-name>] Accepted connection from 172.24.0.4:45452
cloudql-1    | 2024/04/19 14:20:57 [<instance-name>] Now = 2024-04-19T14:20:57Z, Current cert expiration = 2024-04-19T15:20:50Z
cloudql-1    | 2024/04/19 14:20:57 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:20:57 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:20:57.245 UTC [1] LOG S-0xffff81e6deb0: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45452)
pgbouncer-1  | 2024-04-19 14:20:57.245 UTC [1] LOG S-0xffff81e6deb0: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45452)
pgbouncer-1  | 2024-04-19 14:20:57.531 UTC [1] LOG S-0xffff81e6e160: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45468)
pgbouncer-1  | 2024-04-19 14:20:57.531 UTC [1] LOG S-0xffff81e6e160: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45468)
cloudql-1    | 2024/04/19 14:20:57 [<instance-name>] Accepted connection from 172.24.0.4:45468
cloudql-1    | 2024/04/19 14:20:57 [<instance-name>] Now = 2024-04-19T14:20:57Z, Current cert expiration = 2024-04-19T15:20:50Z
cloudql-1    | 2024/04/19 14:20:57 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:20:57 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:20:57.806 UTC [1] LOG S-0xffff81e6e410: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45484)
pgbouncer-1  | 2024-04-19 14:20:57.806 UTC [1] LOG S-0xffff81e6e410: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45484)
cloudql-1    | 2024/04/19 14:20:57 [<instance-name>] Accepted connection from 172.24.0.4:45484
cloudql-1    | 2024/04/19 14:20:57 [<instance-name>] Now = 2024-04-19T14:20:57Z, Current cert expiration = 2024-04-19T15:20:50Z
cloudql-1    | 2024/04/19 14:20:57 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:20:57 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:20:58.083 UTC [1] LOG S-0xffff81e6e6c0: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45486)
pgbouncer-1  | 2024-04-19 14:20:58.083 UTC [1] LOG S-0xffff81e6e6c0: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45486)
cloudql-1    | 2024/04/19 14:20:58 [<instance-name>] Accepted connection from 172.24.0.4:45486
cloudql-1    | 2024/04/19 14:20:58 [<instance-name>] Now = 2024-04-19T14:20:58Z, Current cert expiration = 2024-04-19T15:20:50Z
cloudql-1    | 2024/04/19 14:20:58 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:20:58 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:20:58 [<instance-name>] Accepted connection from 172.24.0.4:45492
cloudql-1    | 2024/04/19 14:20:58 [<instance-name>] Now = 2024-04-19T14:20:58Z, Current cert expiration = 2024-04-19T15:20:50Z
pgbouncer-1  | 2024-04-19 14:20:58.345 UTC [1] LOG S-0xffff81e6e970: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45492)
pgbouncer-1  | 2024-04-19 14:20:58.345 UTC [1] LOG S-0xffff81e6e970: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45492)
cloudql-1    | 2024/04/19 14:20:58 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:20:58 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:20:58.627 UTC [1] LOG S-0xffff81e6ec20: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45500)
pgbouncer-1  | 2024-04-19 14:20:58.627 UTC [1] LOG S-0xffff81e6ec20: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45500)
cloudql-1    | 2024/04/19 14:20:58 [<instance-name>] Accepted connection from 172.24.0.4:45500
cloudql-1    | 2024/04/19 14:20:58 [<instance-name>] Now = 2024-04-19T14:20:58Z, Current cert expiration = 2024-04-19T15:20:50Z
cloudql-1    | 2024/04/19 14:20:58 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:20:58 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:20:58 [<instance-name>] Accepted connection from 172.24.0.4:45512
cloudql-1    | 2024/04/19 14:20:58 [<instance-name>] Now = 2024-04-19T14:20:58Z, Current cert expiration = 2024-04-19T15:20:50Z
cloudql-1    | 2024/04/19 14:20:58 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:20:58 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:20:58.904 UTC [1] LOG S-0xffff81e6eed0: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45512)
pgbouncer-1  | 2024-04-19 14:20:58.904 UTC [1] LOG S-0xffff81e6eed0: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45512)
cloudql-1    | 2024/04/19 14:20:59 [<instance-name>] Accepted connection from 172.24.0.4:45518
cloudql-1    | 2024/04/19 14:20:59 [<instance-name>] Now = 2024-04-19T14:20:59Z, Current cert expiration = 2024-04-19T15:20:50Z
cloudql-1    | 2024/04/19 14:20:59 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:20:59 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:20:59.215 UTC [1] LOG S-0xffff81e6f180: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45518)
pgbouncer-1  | 2024-04-19 14:20:59.215 UTC [1] LOG S-0xffff81e6f180: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45518)
pgbouncer-1  | 2024-04-19 14:20:59.480 UTC [1] LOG S-0xffff81e6f430: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45524)
cloudql-1    | 2024/04/19 14:20:59 [<instance-name>] Accepted connection from 172.24.0.4:45524
pgbouncer-1  | 2024-04-19 14:20:59.480 UTC [1] LOG S-0xffff81e6f430: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45524)
cloudql-1    | 2024/04/19 14:20:59 [<instance-name>] Now = 2024-04-19T14:20:59Z, Current cert expiration = 2024-04-19T15:20:50Z
cloudql-1    | 2024/04/19 14:20:59 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:20:59 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:20:59 [<instance-name>] Accepted connection from 172.24.0.4:45538
cloudql-1    | 2024/04/19 14:20:59 [<instance-name>] Now = 2024-04-19T14:20:59Z, Current cert expiration = 2024-04-19T15:20:50Z
cloudql-1    | 2024/04/19 14:20:59 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:20:59 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:20:59.744 UTC [1] LOG S-0xffff81e6f6e0: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45538)
pgbouncer-1  | 2024-04-19 14:20:59.744 UTC [1] LOG S-0xffff81e6f6e0: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45538)
cloudql-1    | 2024/04/19 14:21:00 [<instance-name>] Accepted connection from 172.24.0.4:45542
cloudql-1    | 2024/04/19 14:21:00 [<instance-name>] Now = 2024-04-19T14:21:00Z, Current cert expiration = 2024-04-19T15:20:50Z
cloudql-1    | 2024/04/19 14:21:00 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:21:00 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:21:00.000 UTC [1] LOG S-0xffff81e6f990: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45542)
pgbouncer-1  | 2024-04-19 14:21:00.000 UTC [1] LOG S-0xffff81e6f990: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45542)
pgbouncer-1  | 2024-04-19 14:21:00.250 UTC [1] LOG S-0xffff81e6fc40: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45548)
pgbouncer-1  | 2024-04-19 14:21:00.250 UTC [1] LOG S-0xffff81e6fc40: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45548)
cloudql-1    | 2024/04/19 14:21:00 [<instance-name>] Accepted connection from 172.24.0.4:45548
cloudql-1    | 2024/04/19 14:21:00 [<instance-name>] Now = 2024-04-19T14:21:00Z, Current cert expiration = 2024-04-19T15:20:50Z
cloudql-1    | 2024/04/19 14:21:00 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:21:00 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:21:00.536 UTC [1] LOG S-0xffff81e6fef0: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45552)
pgbouncer-1  | 2024-04-19 14:21:00.536 UTC [1] LOG S-0xffff81e6fef0: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45552)
cloudql-1    | 2024/04/19 14:21:00 [<instance-name>] Accepted connection from 172.24.0.4:45552
cloudql-1    | 2024/04/19 14:21:00 [<instance-name>] Now = 2024-04-19T14:21:00Z, Current cert expiration = 2024-04-19T15:20:50Z
cloudql-1    | 2024/04/19 14:21:00 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:21:00 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:21:00.800 UTC [1] LOG S-0xffff81e701a0: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45560)
pgbouncer-1  | 2024-04-19 14:21:00.800 UTC [1] LOG S-0xffff81e701a0: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45560)
cloudql-1    | 2024/04/19 14:21:00 [<instance-name>] Accepted connection from 172.24.0.4:45560
cloudql-1    | 2024/04/19 14:21:00 [<instance-name>] Now = 2024-04-19T14:21:00Z, Current cert expiration = 2024-04-19T15:20:50Z
cloudql-1    | 2024/04/19 14:21:00 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:21:00 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:21:01.066 UTC [1] LOG S-0xffff81e70450: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45566)
pgbouncer-1  | 2024-04-19 14:21:01.066 UTC [1] LOG S-0xffff81e70450: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45566)
cloudql-1    | 2024/04/19 14:21:01 [<instance-name>] Accepted connection from 172.24.0.4:45566
cloudql-1    | 2024/04/19 14:21:01 [<instance-name>] Now = 2024-04-19T14:21:01Z, Current cert expiration = 2024-04-19T15:20:50Z
cloudql-1    | 2024/04/19 14:21:01 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:21:01 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:21:01.353 UTC [1] LOG S-0xffff81e70700: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45568)
pgbouncer-1  | 2024-04-19 14:21:01.353 UTC [1] LOG S-0xffff81e70700: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45568)
cloudql-1    | 2024/04/19 14:21:01 [<instance-name>] Accepted connection from 172.24.0.4:45568
cloudql-1    | 2024/04/19 14:21:01 [<instance-name>] Now = 2024-04-19T14:21:01Z, Current cert expiration = 2024-04-19T15:20:50Z
cloudql-1    | 2024/04/19 14:21:01 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:21:01 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:21:01.614 UTC [1] LOG S-0xffff81e709b0: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45582)
pgbouncer-1  | 2024-04-19 14:21:01.614 UTC [1] LOG S-0xffff81e709b0: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45582)
cloudql-1    | 2024/04/19 14:21:01 [<instance-name>] Accepted connection from 172.24.0.4:45582
cloudql-1    | 2024/04/19 14:21:01 [<instance-name>] Now = 2024-04-19T14:21:01Z, Current cert expiration = 2024-04-19T15:20:50Z
cloudql-1    | 2024/04/19 14:21:01 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:21:01 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:21:01.892 UTC [1] LOG S-0xffff81e70c60: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45592)
pgbouncer-1  | 2024-04-19 14:21:01.892 UTC [1] LOG S-0xffff81e70c60: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45592)
cloudql-1    | 2024/04/19 14:21:01 [<instance-name>] Accepted connection from 172.24.0.4:45592
cloudql-1    | 2024/04/19 14:21:01 [<instance-name>] Now = 2024-04-19T14:21:01Z, Current cert expiration = 2024-04-19T15:20:50Z
cloudql-1    | 2024/04/19 14:21:01 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:21:01 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:21:02 [<instance-name>] Accepted connection from 172.24.0.4:45598
cloudql-1    | 2024/04/19 14:21:02 [<instance-name>] Now = 2024-04-19T14:21:02Z, Current cert expiration = 2024-04-19T15:20:50Z
pgbouncer-1  | 2024-04-19 14:21:02.157 UTC [1] LOG S-0xffff81e70f10: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45598)
pgbouncer-1  | 2024-04-19 14:21:02.157 UTC [1] LOG S-0xffff81e70f10: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45598)
cloudql-1    | 2024/04/19 14:21:02 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:21:02 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:21:02 [<instance-name>] Accepted connection from 172.24.0.4:45600
pgbouncer-1  | 2024-04-19 14:21:02.404 UTC [1] LOG S-0xffff81e711c0: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45600)
cloudql-1    | 2024/04/19 14:21:02 [<instance-name>] Now = 2024-04-19T14:21:02Z, Current cert expiration = 2024-04-19T15:20:50Z
cloudql-1    | 2024/04/19 14:21:02 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:21:02 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:21:02.404 UTC [1] LOG S-0xffff81e711c0: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45600)
pgbouncer-1  | 2024-04-19 14:21:02.643 UTC [1] LOG S-0xffff81e71470: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45606)
cloudql-1    | 2024/04/19 14:21:02 [<instance-name>] Accepted connection from 172.24.0.4:45606
pgbouncer-1  | 2024-04-19 14:21:02.643 UTC [1] LOG S-0xffff81e71470: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45606)
cloudql-1    | 2024/04/19 14:21:02 [<instance-name>] Now = 2024-04-19T14:21:02Z, Current cert expiration = 2024-04-19T15:20:50Z
cloudql-1    | 2024/04/19 14:21:02 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:21:02 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:21:02 [<instance-name>] Accepted connection from 172.24.0.4:45610
cloudql-1    | 2024/04/19 14:21:02 [<instance-name>] Now = 2024-04-19T14:21:02Z, Current cert expiration = 2024-04-19T15:20:50Z
cloudql-1    | 2024/04/19 14:21:02 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:21:02 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:21:02.919 UTC [1] LOG S-0xffff81e71720: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45610)
pgbouncer-1  | 2024-04-19 14:21:02.919 UTC [1] LOG S-0xffff81e71720: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45610)
pgbouncer-1  | 2024-04-19 14:21:03.169 UTC [1] LOG S-0xffff81e719d0: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45614)
pgbouncer-1  | 2024-04-19 14:21:03.169 UTC [1] LOG S-0xffff81e719d0: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45614)
cloudql-1    | 2024/04/19 14:21:03 [<instance-name>] Accepted connection from 172.24.0.4:45614
cloudql-1    | 2024/04/19 14:21:03 [<instance-name>] Now = 2024-04-19T14:21:03Z, Current cert expiration = 2024-04-19T15:20:50Z
cloudql-1    | 2024/04/19 14:21:03 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:21:03 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:21:03.444 UTC [1] LOG S-0xffff81e71c80: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45628)
pgbouncer-1  | 2024-04-19 14:21:03.444 UTC [1] LOG S-0xffff81e71c80: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45628)
cloudql-1    | 2024/04/19 14:21:03 [<instance-name>] Accepted connection from 172.24.0.4:45628
cloudql-1    | 2024/04/19 14:21:03 [<instance-name>] Now = 2024-04-19T14:21:03Z, Current cert expiration = 2024-04-19T15:20:50Z
cloudql-1    | 2024/04/19 14:21:03 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:21:03 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:21:03.719 UTC [1] LOG S-0xffff81e71f30: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45634)
pgbouncer-1  | 2024-04-19 14:21:03.719 UTC [1] LOG S-0xffff81e71f30: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45634)
cloudql-1    | 2024/04/19 14:21:03 [<instance-name>] Accepted connection from 172.24.0.4:45634
cloudql-1    | 2024/04/19 14:21:03 [<instance-name>] Now = 2024-04-19T14:21:03Z, Current cert expiration = 2024-04-19T15:20:50Z
cloudql-1    | 2024/04/19 14:21:03 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:21:03 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:21:03 [<instance-name>] Accepted connection from 172.24.0.4:45644
cloudql-1    | 2024/04/19 14:21:03 [<instance-name>] Now = 2024-04-19T14:21:03Z, Current cert expiration = 2024-04-19T15:20:50Z
cloudql-1    | 2024/04/19 14:21:03 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:21:03 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:21:03.998 UTC [1] LOG S-0xffff81e721e0: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45644)
pgbouncer-1  | 2024-04-19 14:21:03.998 UTC [1] LOG S-0xffff81e721e0: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45644)
pgbouncer-1  | 2024-04-19 14:21:04.256 UTC [1] LOG S-0xffff81e72490: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45656)
pgbouncer-1  | 2024-04-19 14:21:04.256 UTC [1] LOG S-0xffff81e72490: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45656)
cloudql-1    | 2024/04/19 14:21:04 [<instance-name>] Accepted connection from 172.24.0.4:45656
cloudql-1    | 2024/04/19 14:21:04 [<instance-name>] Now = 2024-04-19T14:21:04Z, Current cert expiration = 2024-04-19T15:20:50Z
cloudql-1    | 2024/04/19 14:21:04 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:21:04 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:21:04 [<instance-name>] Accepted connection from 172.24.0.4:45662
cloudql-1    | 2024/04/19 14:21:04 [<instance-name>] Now = 2024-04-19T14:21:04Z, Current cert expiration = 2024-04-19T15:20:50Z
cloudql-1    | 2024/04/19 14:21:04 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:21:04 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:21:04.498 UTC [1] LOG S-0xffff81e72740: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45662)
pgbouncer-1  | 2024-04-19 14:21:04.498 UTC [1] LOG S-0xffff81e72740: cloudsql/postgres@172.24.0.3:5432 new connection to server (from 172.24.0.4:45662)
cloudql-1    | 2024/04/19 14:21:06 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:21:06.654 UTC [1] LOG C-0xffff81ec8670: cloudsql/postgres@192.168.65.1:27815 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:06.654 UTC [1] LOG S-0xffff81e6d3f0: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:06.654 UTC [1] LOG C-0xffff81ec8670: cloudsql/postgres@192.168.65.1:27815 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:06.654 UTC [1] LOG S-0xffff81e6d3f0: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:21:06 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:21:06.804 UTC [1] LOG C-0xffff81ec93e0: cloudsql/postgres@192.168.65.1:27821 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:06.804 UTC [1] LOG S-0xffff81e6d6a0: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:06.804 UTC [1] LOG C-0xffff81ec93e0: cloudsql/postgres@192.168.65.1:27821 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:06.804 UTC [1] LOG S-0xffff81e6d6a0: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:07.267 UTC [1] LOG C-0xffff81ec8e80: cloudsql/postgres@192.168.65.1:27818 closing because: client close request (age=11s)
pgbouncer-1  | 2024-04-19 14:21:07.267 UTC [1] LOG S-0xffff81e6d950: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:07.267 UTC [1] LOG C-0xffff81ec8e80: cloudsql/postgres@192.168.65.1:27818 closing because: client close request (age=11s)
pgbouncer-1  | 2024-04-19 14:21:07.267 UTC [1] LOG S-0xffff81e6d950: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:21:07 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:21:07.369 UTC [1] LOG C-0xffff81ecd460: cloudsql/postgres@192.168.65.1:27844 closing because: client close request (age=11s)
pgbouncer-1  | 2024-04-19 14:21:07.369 UTC [1] LOG S-0xffff81e6dc00: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:21:07 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:21:07.369 UTC [1] LOG C-0xffff81ecd460: cloudsql/postgres@192.168.65.1:27844 closing because: client close request (age=11s)
pgbouncer-1  | 2024-04-19 14:21:07.369 UTC [1] LOG S-0xffff81e6dc00: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:07.882 UTC [1] LOG C-0xffff81eca6b0: cloudsql/postgres@192.168.65.1:27827 closing because: client close request (age=11s)
pgbouncer-1  | 2024-04-19 14:21:07.882 UTC [1] LOG S-0xffff81e6deb0: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:07.882 UTC [1] LOG C-0xffff81eca6b0: cloudsql/postgres@192.168.65.1:27827 closing because: client close request (age=11s)
pgbouncer-1  | 2024-04-19 14:21:07.882 UTC [1] LOG S-0xffff81e6deb0: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:21:07 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:21:07 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:21:07.908 UTC [1] LOG C-0xffff81ec9ea0: cloudsql/postgres@192.168.65.1:27824 closing because: client close request (age=11s)
pgbouncer-1  | 2024-04-19 14:21:07.908 UTC [1] LOG S-0xffff81e6e160: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:07.908 UTC [1] LOG C-0xffff81ec9ea0: cloudsql/postgres@192.168.65.1:27824 closing because: client close request (age=11s)
pgbouncer-1  | 2024-04-19 14:21:07.908 UTC [1] LOG S-0xffff81e6e160: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:21:08 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:21:08.203 UTC [1] LOG C-0xffff81ecc9a0: cloudsql/postgres@192.168.65.1:27836 closing because: client close request (age=12s)
pgbouncer-1  | 2024-04-19 14:21:08.203 UTC [1] LOG S-0xffff81e6e410: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:08.203 UTC [1] LOG C-0xffff81ecc9a0: cloudsql/postgres@192.168.65.1:27836 closing because: client close request (age=12s)
pgbouncer-1  | 2024-04-19 14:21:08.203 UTC [1] LOG S-0xffff81e6e410: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:21:08 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:21:08.474 UTC [1] LOG C-0xffff81ecac10: cloudsql/postgres@192.168.65.1:27829 closing because: client close request (age=12s)
pgbouncer-1  | 2024-04-19 14:21:08.474 UTC [1] LOG S-0xffff81e6e6c0: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:08.474 UTC [1] LOG C-0xffff81ecac10: cloudsql/postgres@192.168.65.1:27829 closing because: client close request (age=12s)
pgbouncer-1  | 2024-04-19 14:21:08.474 UTC [1] LOG S-0xffff81e6e6c0: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:21:08 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:21:08.890 UTC [1] LOG C-0xffff81eca400: cloudsql/postgres@192.168.65.1:27826 closing because: client close request (age=12s)
pgbouncer-1  | 2024-04-19 14:21:08.890 UTC [1] LOG S-0xffff81e6e970: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:08.890 UTC [1] LOG C-0xffff81eca400: cloudsql/postgres@192.168.65.1:27826 closing because: client close request (age=12s)
pgbouncer-1  | 2024-04-19 14:21:08.890 UTC [1] LOG S-0xffff81e6e970: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:09.053 UTC [1] LOG C-0xffff81ec9690: cloudsql/postgres@192.168.65.1:27820 closing because: client close request (age=13s)
pgbouncer-1  | 2024-04-19 14:21:09.053 UTC [1] LOG S-0xffff81e6ec20: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:09.053 UTC [1] LOG C-0xffff81ec9690: cloudsql/postgres@192.168.65.1:27820 closing because: client close request (age=13s)
pgbouncer-1  | 2024-04-19 14:21:09.053 UTC [1] LOG S-0xffff81e6ec20: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:21:09 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:21:09 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:21:09.475 UTC [1] LOG C-0xffff81ecbee0: cloudsql/postgres@192.168.65.1:27839 closing because: client close request (age=13s)
pgbouncer-1  | 2024-04-19 14:21:09.475 UTC [1] LOG S-0xffff81e6eed0: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:09.475 UTC [1] LOG C-0xffff81ecbee0: cloudsql/postgres@192.168.65.1:27839 closing because: client close request (age=13s)
pgbouncer-1  | 2024-04-19 14:21:09.475 UTC [1] LOG S-0xffff81e6eed0: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:09.565 UTC [1] LOG C-0xffff81ec9130: cloudsql/postgres@192.168.65.1:27819 closing because: client close request (age=13s)
pgbouncer-1  | 2024-04-19 14:21:09.565 UTC [1] LOG S-0xffff81e6f180: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:09.565 UTC [1] LOG C-0xffff81ec9130: cloudsql/postgres@192.168.65.1:27819 closing because: client close request (age=13s)
pgbouncer-1  | 2024-04-19 14:21:09.565 UTC [1] LOG S-0xffff81e6f180: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:21:09 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:21:10 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:21:10 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:21:10.114 UTC [1] LOG C-0xffff81ec9bf0: cloudsql/postgres@192.168.65.1:27822 closing because: client close request (age=14s)
pgbouncer-1  | 2024-04-19 14:21:10.114 UTC [1] LOG S-0xffff81e6f430: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:10.114 UTC [1] LOG C-0xffff81ecd1b0: cloudsql/postgres@192.168.65.1:27842 closing because: client close request (age=14s)
pgbouncer-1  | 2024-04-19 14:21:10.114 UTC [1] LOG S-0xffff81e6f6e0: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:10.114 UTC [1] LOG C-0xffff81ec9bf0: cloudsql/postgres@192.168.65.1:27822 closing because: client close request (age=14s)
pgbouncer-1  | 2024-04-19 14:21:10.114 UTC [1] LOG S-0xffff81e6f430: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:10.114 UTC [1] LOG C-0xffff81ecd1b0: cloudsql/postgres@192.168.65.1:27842 closing because: client close request (age=14s)
pgbouncer-1  | 2024-04-19 14:21:10.114 UTC [1] LOG S-0xffff81e6f6e0: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:21:10 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:21:10.361 UTC [1] LOG C-0xffff81ec83c0: cloudsql/postgres@192.168.65.1:27814 closing because: client close request (age=14s)
pgbouncer-1  | 2024-04-19 14:21:10.361 UTC [1] LOG S-0xffff81e6f990: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:10.361 UTC [1] LOG C-0xffff81ec83c0: cloudsql/postgres@192.168.65.1:27814 closing because: client close request (age=14s)
pgbouncer-1  | 2024-04-19 14:21:10.361 UTC [1] LOG S-0xffff81e6f990: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:10.625 UTC [1] LOG C-0xffff81ec9940: cloudsql/postgres@192.168.65.1:27823 closing because: client close request (age=14s)
pgbouncer-1  | 2024-04-19 14:21:10.625 UTC [1] LOG S-0xffff81e6fc40: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:10.625 UTC [1] LOG C-0xffff81ec9940: cloudsql/postgres@192.168.65.1:27823 closing because: client close request (age=14s)
pgbouncer-1  | 2024-04-19 14:21:10.625 UTC [1] LOG S-0xffff81e6fc40: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:21:10 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:21:10.908 UTC [1] LOG C-0xffff81eca960: cloudsql/postgres@192.168.65.1:27828 closing because: client close request (age=14s)
pgbouncer-1  | 2024-04-19 14:21:10.908 UTC [1] LOG S-0xffff81e6fef0: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:21:10 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:21:10.908 UTC [1] LOG C-0xffff81eca960: cloudsql/postgres@192.168.65.1:27828 closing because: client close request (age=14s)
pgbouncer-1  | 2024-04-19 14:21:10.908 UTC [1] LOG S-0xffff81e6fef0: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:11.191 UTC [1] LOG C-0xffff81ecb420: cloudsql/postgres@192.168.65.1:27832 closing because: client close request (age=15s)
pgbouncer-1  | 2024-04-19 14:21:11.191 UTC [1] LOG S-0xffff81e701a0: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:11.191 UTC [1] LOG C-0xffff81ecb420: cloudsql/postgres@192.168.65.1:27832 closing because: client close request (age=15s)
pgbouncer-1  | 2024-04-19 14:21:11.191 UTC [1] LOG S-0xffff81e701a0: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:21:11 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:21:11 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:21:11.463 UTC [1] LOG C-0xffff81eccc50: cloudsql/postgres@192.168.65.1:27838 closing because: client close request (age=15s)
pgbouncer-1  | 2024-04-19 14:21:11.463 UTC [1] LOG S-0xffff81e70450: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:11.463 UTC [1] LOG C-0xffff81eccc50: cloudsql/postgres@192.168.65.1:27838 closing because: client close request (age=15s)
pgbouncer-1  | 2024-04-19 14:21:11.463 UTC [1] LOG S-0xffff81e70450: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:11.717 UTC [1] LOG C-0xffff81eccf00: cloudsql/postgres@192.168.65.1:27840 closing because: client close request (age=15s)
pgbouncer-1  | 2024-04-19 14:21:11.717 UTC [1] LOG S-0xffff81e70700: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:11.717 UTC [1] LOG C-0xffff81eccf00: cloudsql/postgres@192.168.65.1:27840 closing because: client close request (age=15s)
pgbouncer-1  | 2024-04-19 14:21:11.717 UTC [1] LOG S-0xffff81e70700: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:21:11 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:21:11.994 UTC [1] LOG C-0xffff81eca150: cloudsql/postgres@192.168.65.1:27825 closing because: client close request (age=16s)
pgbouncer-1  | 2024-04-19 14:21:11.994 UTC [1] LOG S-0xffff81e709b0: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:11.994 UTC [1] LOG C-0xffff81eca150: cloudsql/postgres@192.168.65.1:27825 closing because: client close request (age=16s)
pgbouncer-1  | 2024-04-19 14:21:11.994 UTC [1] LOG S-0xffff81e709b0: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:21:11 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:21:12.255 UTC [1] LOG C-0xffff81ec8920: cloudsql/postgres@192.168.65.1:27816 closing because: client close request (age=16s)
pgbouncer-1  | 2024-04-19 14:21:12.256 UTC [1] LOG S-0xffff81e70c60: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:12.255 UTC [1] LOG C-0xffff81ec8920: cloudsql/postgres@192.168.65.1:27816 closing because: client close request (age=16s)
pgbouncer-1  | 2024-04-19 14:21:12.256 UTC [1] LOG S-0xffff81e70c60: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:21:12 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:21:12.521 UTC [1] LOG C-0xffff81ecaec0: cloudsql/postgres@192.168.65.1:27830 closing because: client close request (age=16s)
pgbouncer-1  | 2024-04-19 14:21:12.521 UTC [1] LOG S-0xffff81e70f10: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:12.521 UTC [1] LOG C-0xffff81ecaec0: cloudsql/postgres@192.168.65.1:27830 closing because: client close request (age=16s)
pgbouncer-1  | 2024-04-19 14:21:12.521 UTC [1] LOG S-0xffff81e70f10: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:21:12 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:21:12.757 UTC [1] LOG C-0xffff81ecb170: cloudsql/postgres@192.168.65.1:27831 closing because: client close request (age=16s)
pgbouncer-1  | 2024-04-19 14:21:12.757 UTC [1] LOG S-0xffff81e711c0: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:12.757 UTC [1] LOG C-0xffff81ecb170: cloudsql/postgres@192.168.65.1:27831 closing because: client close request (age=16s)
pgbouncer-1  | 2024-04-19 14:21:12.757 UTC [1] LOG S-0xffff81e711c0: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:21:12 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:21:13 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:21:13.011 UTC [1] LOG C-0xffff81ecc190: cloudsql/postgres@192.168.65.1:27841 closing because: client close request (age=17s)
pgbouncer-1  | 2024-04-19 14:21:13.011 UTC [1] LOG S-0xffff81e71470: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:13.011 UTC [1] LOG C-0xffff81ecc190: cloudsql/postgres@192.168.65.1:27841 closing because: client close request (age=17s)
pgbouncer-1  | 2024-04-19 14:21:13.011 UTC [1] LOG S-0xffff81e71470: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:21:13 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:21:13.264 UTC [1] LOG C-0xffff81ecc6f0: cloudsql/postgres@192.168.65.1:27834 closing because: client close request (age=17s)
pgbouncer-1  | 2024-04-19 14:21:13.265 UTC [1] LOG S-0xffff81e71720: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:13.264 UTC [1] LOG C-0xffff81ecc6f0: cloudsql/postgres@192.168.65.1:27834 closing because: client close request (age=17s)
pgbouncer-1  | 2024-04-19 14:21:13.265 UTC [1] LOG S-0xffff81e71720: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:13.565 UTC [1] LOG C-0xffff81ecc440: cloudsql/postgres@192.168.65.1:27843 closing because: client close request (age=17s)
pgbouncer-1  | 2024-04-19 14:21:13.565 UTC [1] LOG S-0xffff81e719d0: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:21:13 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:21:13.565 UTC [1] LOG C-0xffff81ecc440: cloudsql/postgres@192.168.65.1:27843 closing because: client close request (age=17s)
pgbouncer-1  | 2024-04-19 14:21:13.565 UTC [1] LOG S-0xffff81e719d0: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:13.941 UTC [1] LOG C-0xffff81ecb6d0: cloudsql/postgres@192.168.65.1:27833 closing because: client close request (age=18s)
pgbouncer-1  | 2024-04-19 14:21:13.941 UTC [1] LOG S-0xffff81e71c80: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:13.941 UTC [1] LOG C-0xffff81ecb6d0: cloudsql/postgres@192.168.65.1:27833 closing because: client close request (age=18s)
pgbouncer-1  | 2024-04-19 14:21:13.941 UTC [1] LOG S-0xffff81e71c80: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:21:13 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:21:14.100 UTC [1] LOG C-0xffff81ecd710: cloudsql/postgres@192.168.65.1:27845 closing because: client close request (age=18s)
pgbouncer-1  | 2024-04-19 14:21:14.100 UTC [1] LOG S-0xffff81e71f30: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:14.100 UTC [1] LOG C-0xffff81ecd710: cloudsql/postgres@192.168.65.1:27845 closing because: client close request (age=18s)
pgbouncer-1  | 2024-04-19 14:21:14.100 UTC [1] LOG S-0xffff81e71f30: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:21:14 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:21:14 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:21:14.343 UTC [1] LOG C-0xffff81ecbc30: cloudsql/postgres@192.168.65.1:27837 closing because: client close request (age=18s)
pgbouncer-1  | 2024-04-19 14:21:14.343 UTC [1] LOG S-0xffff81e721e0: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:14.343 UTC [1] LOG C-0xffff81ecbc30: cloudsql/postgres@192.168.65.1:27837 closing because: client close request (age=18s)
pgbouncer-1  | 2024-04-19 14:21:14.343 UTC [1] LOG S-0xffff81e721e0: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:14.739 UTC [1] LOG C-0xffff81ecb980: cloudsql/postgres@192.168.65.1:27835 closing because: client close request (age=18s)
pgbouncer-1  | 2024-04-19 14:21:14.739 UTC [1] LOG S-0xffff81e72490: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:14.739 UTC [1] LOG C-0xffff81ecb980: cloudsql/postgres@192.168.65.1:27835 closing because: client close request (age=18s)
pgbouncer-1  | 2024-04-19 14:21:14.739 UTC [1] LOG S-0xffff81e72490: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:21:14 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:21:14.845 UTC [1] LOG C-0xffff81ec8bd0: cloudsql/postgres@192.168.65.1:27817 closing because: client close request (age=18s)
pgbouncer-1  | 2024-04-19 14:21:14.845 UTC [1] LOG S-0xffff81e72740: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:14.845 UTC [1] LOG C-0xffff81ec8bd0: cloudsql/postgres@192.168.65.1:27817 closing because: client close request (age=18s)
pgbouncer-1  | 2024-04-19 14:21:14.845 UTC [1] LOG S-0xffff81e72740: cloudsql/postgres@172.24.0.3:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:21:14 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:21:14.881 UTC [1] LOG C-0xffff81ecb980: local/postgres@192.168.65.1:27891 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.881 UTC [1] LOG C-0xffff81ec8bd0: local/postgres@192.168.65.1:27890 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.881 UTC [1] LOG C-0xffff81ecb6d0: local/postgres@192.168.65.1:27894 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.881 UTC [1] LOG C-0xffff81ecbc30: local/postgres@192.168.65.1:27892 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.881 UTC [1] LOG C-0xffff81ecd710: local/postgres@192.168.65.1:27893 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.881 UTC [1] LOG C-0xffff81ecc190: local/postgres@192.168.65.1:27897 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.881 UTC [1] LOG C-0xffff81ecc6f0: local/postgres@192.168.65.1:27896 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.881 UTC [1] LOG C-0xffff81ecc440: local/postgres@192.168.65.1:27895 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.881 UTC [1] LOG C-0xffff81eca150: local/postgres@192.168.65.1:27901 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.881 UTC [1] LOG C-0xffff81ec8920: local/postgres@192.168.65.1:27899 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.881 UTC [1] LOG C-0xffff81ecb980: local/postgres@192.168.65.1:27891 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.881 UTC [1] LOG C-0xffff81ec8bd0: local/postgres@192.168.65.1:27890 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.881 UTC [1] LOG C-0xffff81ecb6d0: local/postgres@192.168.65.1:27894 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.881 UTC [1] LOG C-0xffff81ecbc30: local/postgres@192.168.65.1:27892 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.881 UTC [1] LOG C-0xffff81ecd710: local/postgres@192.168.65.1:27893 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.881 UTC [1] LOG C-0xffff81ecc190: local/postgres@192.168.65.1:27897 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.881 UTC [1] LOG C-0xffff81ecc6f0: local/postgres@192.168.65.1:27896 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.881 UTC [1] LOG C-0xffff81ecc440: local/postgres@192.168.65.1:27895 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.881 UTC [1] LOG C-0xffff81eca150: local/postgres@192.168.65.1:27901 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.881 UTC [1] LOG C-0xffff81ec8920: local/postgres@192.168.65.1:27899 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81ecaec0: local/postgres@192.168.65.1:27898 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81ecb170: local/postgres@192.168.65.1:27900 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81ec9940: local/postgres@192.168.65.1:27906 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81eca960: local/postgres@192.168.65.1:27905 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81ecd1b0: local/postgres@192.168.65.1:27908 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81ecb420: local/postgres@192.168.65.1:27904 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81ec83c0: local/postgres@192.168.65.1:27907 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81eccc50: local/postgres@192.168.65.1:27903 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81ec9690: local/postgres@192.168.65.1:27912 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81eccf00: local/postgres@192.168.65.1:27902 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81eca400: local/postgres@192.168.65.1:27913 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81ecbee0: local/postgres@192.168.65.1:27911 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81ecac10: local/postgres@192.168.65.1:27914 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81ec9130: local/postgres@192.168.65.1:27910 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81ec9bf0: local/postgres@192.168.65.1:27909 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81eca6b0: local/postgres@192.168.65.1:27917 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81ecaec0: local/postgres@192.168.65.1:27898 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81ecb170: local/postgres@192.168.65.1:27900 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81ec9940: local/postgres@192.168.65.1:27906 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81eca960: local/postgres@192.168.65.1:27905 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81ecd1b0: local/postgres@192.168.65.1:27908 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81ecb420: local/postgres@192.168.65.1:27904 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81ec83c0: local/postgres@192.168.65.1:27907 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81eccc50: local/postgres@192.168.65.1:27903 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81ec9690: local/postgres@192.168.65.1:27912 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81eccf00: local/postgres@192.168.65.1:27902 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81eca400: local/postgres@192.168.65.1:27913 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81ecbee0: local/postgres@192.168.65.1:27911 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81ecac10: local/postgres@192.168.65.1:27914 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81ec9130: local/postgres@192.168.65.1:27910 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81ec9bf0: local/postgres@192.168.65.1:27909 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81eca6b0: local/postgres@192.168.65.1:27917 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81ec9ea0: local/postgres@192.168.65.1:27916 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81ecc9a0: local/postgres@192.168.65.1:27915 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81ec8e80: local/postgres@192.168.65.1:27919 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81ecd460: local/postgres@192.168.65.1:27918 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81ec8670: local/postgres@192.168.65.1:27921 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81ec93e0: local/postgres@192.168.65.1:27920 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81ec9ea0: local/postgres@192.168.65.1:27916 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81ecc9a0: local/postgres@192.168.65.1:27915 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81ec8e80: local/postgres@192.168.65.1:27919 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81ecd460: local/postgres@192.168.65.1:27918 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81ec8670: local/postgres@192.168.65.1:27921 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:14.882 UTC [1] LOG C-0xffff81ec93e0: local/postgres@192.168.65.1:27920 login attempt: db=local user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:21:15.010 UTC [1] LOG S-0xffff81e72740: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46462)
pgbouncer-1  | 2024-04-19 14:21:15.010 UTC [1] LOG S-0xffff81e72740: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46462)
pgbouncer-1  | 2024-04-19 14:21:15.017 UTC [1] LOG S-0xffff81e72490: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46470)
pgbouncer-1  | 2024-04-19 14:21:15.017 UTC [1] LOG S-0xffff81e72490: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46470)
pgbouncer-1  | 2024-04-19 14:21:15.024 UTC [1] LOG S-0xffff81e721e0: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46482)
pgbouncer-1  | 2024-04-19 14:21:15.024 UTC [1] LOG S-0xffff81e721e0: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46482)
pgbouncer-1  | 2024-04-19 14:21:15.030 UTC [1] LOG S-0xffff81e71f30: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46496)
pgbouncer-1  | 2024-04-19 14:21:15.030 UTC [1] LOG S-0xffff81e71f30: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46496)
pgbouncer-1  | 2024-04-19 14:21:15.035 UTC [1] LOG S-0xffff81e71c80: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46504)
pgbouncer-1  | 2024-04-19 14:21:15.035 UTC [1] LOG S-0xffff81e71c80: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46504)
pgbouncer-1  | 2024-04-19 14:21:15.041 UTC [1] LOG S-0xffff81e719d0: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46512)
pgbouncer-1  | 2024-04-19 14:21:15.041 UTC [1] LOG S-0xffff81e719d0: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46512)
pgbouncer-1  | 2024-04-19 14:21:15.046 UTC [1] LOG S-0xffff81e71720: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46518)
pgbouncer-1  | 2024-04-19 14:21:15.046 UTC [1] LOG S-0xffff81e71720: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46518)
pgbouncer-1  | 2024-04-19 14:21:15.052 UTC [1] LOG S-0xffff81e71470: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46528)
pgbouncer-1  | 2024-04-19 14:21:15.052 UTC [1] LOG S-0xffff81e71470: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46528)
pgbouncer-1  | 2024-04-19 14:21:15.058 UTC [1] LOG S-0xffff81e711c0: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46544)
pgbouncer-1  | 2024-04-19 14:21:15.058 UTC [1] LOG S-0xffff81e711c0: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46544)
pgbouncer-1  | 2024-04-19 14:21:15.063 UTC [1] LOG S-0xffff81e70f10: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46546)
pgbouncer-1  | 2024-04-19 14:21:15.063 UTC [1] LOG S-0xffff81e70f10: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46546)
pgbouncer-1  | 2024-04-19 14:21:15.069 UTC [1] LOG S-0xffff81e70c60: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46558)
pgbouncer-1  | 2024-04-19 14:21:15.069 UTC [1] LOG S-0xffff81e70c60: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46558)
pgbouncer-1  | 2024-04-19 14:21:15.075 UTC [1] LOG S-0xffff81e709b0: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46562)
pgbouncer-1  | 2024-04-19 14:21:15.075 UTC [1] LOG S-0xffff81e709b0: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46562)
pgbouncer-1  | 2024-04-19 14:21:15.080 UTC [1] LOG S-0xffff81e70700: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46578)
pgbouncer-1  | 2024-04-19 14:21:15.080 UTC [1] LOG S-0xffff81e70700: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46578)
pgbouncer-1  | 2024-04-19 14:21:15.085 UTC [1] LOG S-0xffff81e70450: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46594)
pgbouncer-1  | 2024-04-19 14:21:15.085 UTC [1] LOG S-0xffff81e70450: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46594)
pgbouncer-1  | 2024-04-19 14:21:15.091 UTC [1] LOG S-0xffff81e701a0: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46596)
pgbouncer-1  | 2024-04-19 14:21:15.091 UTC [1] LOG S-0xffff81e701a0: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46596)
pgbouncer-1  | 2024-04-19 14:21:15.096 UTC [1] LOG S-0xffff81e6fef0: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46612)
pgbouncer-1  | 2024-04-19 14:21:15.096 UTC [1] LOG S-0xffff81e6fef0: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46612)
pgbouncer-1  | 2024-04-19 14:21:15.102 UTC [1] LOG S-0xffff81e6fc40: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46624)
pgbouncer-1  | 2024-04-19 14:21:15.102 UTC [1] LOG S-0xffff81e6fc40: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46624)
pgbouncer-1  | 2024-04-19 14:21:15.107 UTC [1] LOG S-0xffff81e6f990: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46628)
pgbouncer-1  | 2024-04-19 14:21:15.107 UTC [1] LOG S-0xffff81e6f990: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46628)
pgbouncer-1  | 2024-04-19 14:21:15.113 UTC [1] LOG S-0xffff81e6f6e0: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46636)
pgbouncer-1  | 2024-04-19 14:21:15.113 UTC [1] LOG S-0xffff81e6f6e0: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46636)
pgbouncer-1  | 2024-04-19 14:21:15.118 UTC [1] LOG S-0xffff81e6f430: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46638)
pgbouncer-1  | 2024-04-19 14:21:15.118 UTC [1] LOG S-0xffff81e6f430: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46638)
pgbouncer-1  | 2024-04-19 14:21:15.124 UTC [1] LOG S-0xffff81e6f180: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46642)
pgbouncer-1  | 2024-04-19 14:21:15.124 UTC [1] LOG S-0xffff81e6f180: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46642)
pgbouncer-1  | 2024-04-19 14:21:15.130 UTC [1] LOG S-0xffff81e6eed0: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46644)
pgbouncer-1  | 2024-04-19 14:21:15.130 UTC [1] LOG S-0xffff81e6eed0: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46644)
pgbouncer-1  | 2024-04-19 14:21:15.136 UTC [1] LOG S-0xffff81e6ec20: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46648)
pgbouncer-1  | 2024-04-19 14:21:15.136 UTC [1] LOG S-0xffff81e6ec20: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46648)
pgbouncer-1  | 2024-04-19 14:21:15.141 UTC [1] LOG S-0xffff81e6e970: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46652)
pgbouncer-1  | 2024-04-19 14:21:15.141 UTC [1] LOG S-0xffff81e6e970: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46652)
pgbouncer-1  | 2024-04-19 14:21:15.147 UTC [1] LOG S-0xffff81e6e6c0: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46668)
pgbouncer-1  | 2024-04-19 14:21:15.147 UTC [1] LOG S-0xffff81e6e6c0: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46668)
pgbouncer-1  | 2024-04-19 14:21:15.152 UTC [1] LOG S-0xffff81e6e410: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46682)
pgbouncer-1  | 2024-04-19 14:21:15.152 UTC [1] LOG S-0xffff81e6e410: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46682)
pgbouncer-1  | 2024-04-19 14:21:15.158 UTC [1] LOG S-0xffff81e6e160: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46694)
pgbouncer-1  | 2024-04-19 14:21:15.158 UTC [1] LOG S-0xffff81e6e160: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46694)
pgbouncer-1  | 2024-04-19 14:21:15.164 UTC [1] LOG S-0xffff81e6deb0: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46704)
pgbouncer-1  | 2024-04-19 14:21:15.164 UTC [1] LOG S-0xffff81e6deb0: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46704)
pgbouncer-1  | 2024-04-19 14:21:15.169 UTC [1] LOG S-0xffff81e6dc00: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46708)
pgbouncer-1  | 2024-04-19 14:21:15.169 UTC [1] LOG S-0xffff81e6dc00: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46708)
pgbouncer-1  | 2024-04-19 14:21:15.175 UTC [1] LOG S-0xffff81e6d950: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46718)
pgbouncer-1  | 2024-04-19 14:21:15.175 UTC [1] LOG S-0xffff81e6d950: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46718)
pgbouncer-1  | 2024-04-19 14:21:15.181 UTC [1] LOG S-0xffff81e6d6a0: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46720)
pgbouncer-1  | 2024-04-19 14:21:15.181 UTC [1] LOG S-0xffff81e6d6a0: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46720)
pgbouncer-1  | 2024-04-19 14:21:15.186 UTC [1] LOG S-0xffff81e6d3f0: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46736)
pgbouncer-1  | 2024-04-19 14:21:15.186 UTC [1] LOG S-0xffff81e6d3f0: local/postgres@172.24.0.2:5432 new connection to server (from 172.24.0.4:46736)
pgbouncer-1  | 2024-04-19 14:21:25.034 UTC [1] LOG C-0xffff81ecd710: local/postgres@192.168.65.1:27893 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.034 UTC [1] LOG S-0xffff81e72740: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.034 UTC [1] LOG C-0xffff81ecbc30: local/postgres@192.168.65.1:27892 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.034 UTC [1] LOG S-0xffff81e72490: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.034 UTC [1] LOG C-0xffff81ecd710: local/postgres@192.168.65.1:27893 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.034 UTC [1] LOG S-0xffff81e72740: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.034 UTC [1] LOG C-0xffff81ecbc30: local/postgres@192.168.65.1:27892 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.034 UTC [1] LOG S-0xffff81e72490: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.043 UTC [1] LOG C-0xffff81ecb980: local/postgres@192.168.65.1:27891 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.044 UTC [1] LOG S-0xffff81e721e0: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.043 UTC [1] LOG C-0xffff81ecb980: local/postgres@192.168.65.1:27891 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.044 UTC [1] LOG S-0xffff81e721e0: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.048 UTC [1] LOG C-0xffff81ec8920: local/postgres@192.168.65.1:27899 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.048 UTC [1] LOG S-0xffff81e71f30: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.048 UTC [1] LOG C-0xffff81ec8920: local/postgres@192.168.65.1:27899 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.048 UTC [1] LOG S-0xffff81e71f30: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.053 UTC [1] LOG C-0xffff81ec9690: local/postgres@192.168.65.1:27912 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.053 UTC [1] LOG S-0xffff81e71c80: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.053 UTC [1] LOG C-0xffff81ec9690: local/postgres@192.168.65.1:27912 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.053 UTC [1] LOG S-0xffff81e71c80: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.056 UTC [1] LOG C-0xffff81eccc50: local/postgres@192.168.65.1:27903 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.056 UTC [1] LOG S-0xffff81e71720: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.056 UTC [1] LOG C-0xffff81eccc50: local/postgres@192.168.65.1:27903 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.056 UTC [1] LOG S-0xffff81e71720: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.060 UTC [1] LOG C-0xffff81eca400: local/postgres@192.168.65.1:27913 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.060 UTC [1] LOG S-0xffff81e719d0: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.060 UTC [1] LOG C-0xffff81eca400: local/postgres@192.168.65.1:27913 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.060 UTC [1] LOG S-0xffff81e719d0: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.061 UTC [1] LOG C-0xffff81ecb6d0: local/postgres@192.168.65.1:27894 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.061 UTC [1] LOG S-0xffff81e71470: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.061 UTC [1] LOG C-0xffff81ecb6d0: local/postgres@192.168.65.1:27894 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.061 UTC [1] LOG S-0xffff81e71470: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.076 UTC [1] LOG C-0xffff81ec9ea0: local/postgres@192.168.65.1:27916 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.076 UTC [1] LOG S-0xffff81e711c0: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.076 UTC [1] LOG C-0xffff81ec9ea0: local/postgres@192.168.65.1:27916 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.076 UTC [1] LOG S-0xffff81e711c0: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.082 UTC [1] LOG C-0xffff81ec8bd0: local/postgres@192.168.65.1:27890 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.083 UTC [1] LOG S-0xffff81e70f10: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.082 UTC [1] LOG C-0xffff81ec8bd0: local/postgres@192.168.65.1:27890 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.083 UTC [1] LOG S-0xffff81e70f10: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.091 UTC [1] LOG C-0xffff81ecc440: local/postgres@192.168.65.1:27895 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.091 UTC [1] LOG S-0xffff81e70c60: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.091 UTC [1] LOG C-0xffff81ec9bf0: local/postgres@192.168.65.1:27909 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.091 UTC [1] LOG S-0xffff81e709b0: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.091 UTC [1] LOG C-0xffff81ecc440: local/postgres@192.168.65.1:27895 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.091 UTC [1] LOG S-0xffff81e70c60: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.091 UTC [1] LOG C-0xffff81ec9bf0: local/postgres@192.168.65.1:27909 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.091 UTC [1] LOG S-0xffff81e709b0: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.097 UTC [1] LOG C-0xffff81ecac10: local/postgres@192.168.65.1:27914 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.097 UTC [1] LOG S-0xffff81e70450: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.097 UTC [1] LOG C-0xffff81ecac10: local/postgres@192.168.65.1:27914 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.097 UTC [1] LOG S-0xffff81e70450: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.099 UTC [1] LOG C-0xffff81eca150: local/postgres@192.168.65.1:27901 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.099 UTC [1] LOG S-0xffff81e70700: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.099 UTC [1] LOG C-0xffff81eca150: local/postgres@192.168.65.1:27901 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.099 UTC [1] LOG S-0xffff81e70700: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.102 UTC [1] LOG C-0xffff81ecb420: local/postgres@192.168.65.1:27904 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.102 UTC [1] LOG S-0xffff81e701a0: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.102 UTC [1] LOG C-0xffff81ecb420: local/postgres@192.168.65.1:27904 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.102 UTC [1] LOG S-0xffff81e701a0: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.119 UTC [1] LOG C-0xffff81ecc190: local/postgres@192.168.65.1:27897 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.119 UTC [1] LOG S-0xffff81e6fef0: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.119 UTC [1] LOG C-0xffff81ecc190: local/postgres@192.168.65.1:27897 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.119 UTC [1] LOG S-0xffff81e6fef0: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.124 UTC [1] LOG C-0xffff81eccf00: local/postgres@192.168.65.1:27902 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.124 UTC [1] LOG S-0xffff81e6fc40: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.124 UTC [1] LOG C-0xffff81eccf00: local/postgres@192.168.65.1:27902 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.124 UTC [1] LOG S-0xffff81e6fc40: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.127 UTC [1] LOG C-0xffff81eca6b0: local/postgres@192.168.65.1:27917 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.127 UTC [1] LOG S-0xffff81e6f990: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.127 UTC [1] LOG C-0xffff81eca6b0: local/postgres@192.168.65.1:27917 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.127 UTC [1] LOG S-0xffff81e6f990: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.127 UTC [1] LOG C-0xffff81ec93e0: local/postgres@192.168.65.1:27920 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.127 UTC [1] LOG S-0xffff81e6f6e0: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.127 UTC [1] LOG C-0xffff81ec93e0: local/postgres@192.168.65.1:27920 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.127 UTC [1] LOG S-0xffff81e6f6e0: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.136 UTC [1] LOG C-0xffff81ec83c0: local/postgres@192.168.65.1:27907 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.136 UTC [1] LOG S-0xffff81e6f430: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.136 UTC [1] LOG C-0xffff81ec83c0: local/postgres@192.168.65.1:27907 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.136 UTC [1] LOG S-0xffff81e6f430: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.138 UTC [1] LOG C-0xffff81ec9130: local/postgres@192.168.65.1:27910 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.138 UTC [1] LOG S-0xffff81e6eed0: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.138 UTC [1] LOG C-0xffff81ec9130: local/postgres@192.168.65.1:27910 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.138 UTC [1] LOG S-0xffff81e6eed0: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.138 UTC [1] LOG C-0xffff81ecd1b0: local/postgres@192.168.65.1:27908 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.138 UTC [1] LOG S-0xffff81e6f180: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.138 UTC [1] LOG C-0xffff81ecd1b0: local/postgres@192.168.65.1:27908 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.138 UTC [1] LOG S-0xffff81e6f180: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.158 UTC [1] LOG C-0xffff81ec9940: local/postgres@192.168.65.1:27906 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.158 UTC [1] LOG S-0xffff81e6e6c0: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.158 UTC [1] LOG C-0xffff81ec9940: local/postgres@192.168.65.1:27906 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.158 UTC [1] LOG S-0xffff81e6e6c0: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.173 UTC [1] LOG C-0xffff81ecb170: local/postgres@192.168.65.1:27900 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.173 UTC [1] LOG S-0xffff81e6ec20: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.173 UTC [1] LOG C-0xffff81ecb170: local/postgres@192.168.65.1:27900 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.173 UTC [1] LOG S-0xffff81e6ec20: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.174 UTC [1] LOG C-0xffff81eca960: local/postgres@192.168.65.1:27905 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.174 UTC [1] LOG S-0xffff81e6e970: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.174 UTC [1] LOG C-0xffff81ecaec0: local/postgres@192.168.65.1:27898 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.174 UTC [1] LOG S-0xffff81e6e410: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.174 UTC [1] LOG C-0xffff81eca960: local/postgres@192.168.65.1:27905 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.174 UTC [1] LOG S-0xffff81e6e970: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.174 UTC [1] LOG C-0xffff81ecaec0: local/postgres@192.168.65.1:27898 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.174 UTC [1] LOG S-0xffff81e6e410: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.175 UTC [1] LOG C-0xffff81ec8e80: local/postgres@192.168.65.1:27919 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.175 UTC [1] LOG S-0xffff81e6deb0: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.175 UTC [1] LOG C-0xffff81ec8e80: local/postgres@192.168.65.1:27919 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.175 UTC [1] LOG S-0xffff81e6deb0: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.175 UTC [1] LOG C-0xffff81ec8670: local/postgres@192.168.65.1:27921 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.175 UTC [1] LOG S-0xffff81e6e160: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.175 UTC [1] LOG C-0xffff81ec8670: local/postgres@192.168.65.1:27921 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.175 UTC [1] LOG S-0xffff81e6e160: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.187 UTC [1] LOG C-0xffff81ecc9a0: local/postgres@192.168.65.1:27915 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.187 UTC [1] LOG S-0xffff81e6dc00: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.187 UTC [1] LOG C-0xffff81ecc9a0: local/postgres@192.168.65.1:27915 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.187 UTC [1] LOG S-0xffff81e6dc00: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.192 UTC [1] LOG C-0xffff81ecbee0: local/postgres@192.168.65.1:27911 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.192 UTC [1] LOG S-0xffff81e6d950: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.192 UTC [1] LOG C-0xffff81ecbee0: local/postgres@192.168.65.1:27911 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.192 UTC [1] LOG S-0xffff81e6d950: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.199 UTC [1] LOG C-0xffff81ecd460: local/postgres@192.168.65.1:27918 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.199 UTC [1] LOG S-0xffff81e6d6a0: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.199 UTC [1] LOG C-0xffff81ecd460: local/postgres@192.168.65.1:27918 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.199 UTC [1] LOG S-0xffff81e6d6a0: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.205 UTC [1] LOG C-0xffff81ecc6f0: local/postgres@192.168.65.1:27896 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.205 UTC [1] LOG S-0xffff81e6d3f0: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.205 UTC [1] LOG C-0xffff81ecc6f0: local/postgres@192.168.65.1:27896 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:21:25.205 UTC [1] LOG S-0xffff81e6d3f0: local/postgres@172.24.0.2:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:21:50.567 UTC [1] LOG stats: 1 xacts/s, 2 queries/s, 0 client parses/s, 0 server parses/s, 0 binds/s, in 81 B/s, out 103 B/s, xact 0 us, query 6125672 us, wait 2509366 us
pgbouncer-1  | 2024-04-19 14:21:50.567 UTC [1] LOG stats: 1 xacts/s, 2 queries/s, 0 client parses/s, 0 server parses/s, 0 binds/s, in 81 B/s, out 103 B/s, xact 0 us, query 6125672 us, wait 2509366 us
```
