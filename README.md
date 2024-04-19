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
['10.85s', '10.86s', '11.12s', '11.77s', '11.80s', '11.97s', '12.28s', '12.60s', '12.89s', '13.07s', '14.37s', '14.66s', '14.97s', '15.25s', '15.54s', '15.83s', '16.09s', '16.37s', '16.64s', '16.99s', '17.26s', '17.85s', '17.85s', '18.06s', '18.34s', '18.58s', '18.87s', '19.15s', '19.76s', '19.76s', '19.97s', '20.34s']


postgres://postgres:postgres@127.0.0.1:5433/postgres:
['10.79s', '10.79s', '10.79s', '10.79s', '10.80s', '10.79s', '10.79s', '10.80s', '10.79s', '10.80s', '10.79s', '10.79s', '10.80s', '10.80s', '10.80s', '10.79s', '10.79s', '10.80s', '10.79s', '10.80s', '10.79s', '10.80s', '10.79s', '10.79s', '10.79s', '10.79s', '10.79s', '10.79s', '10.80s', '10.79s', '10.80s', '10.80s']


postgres://postgres:postgres@127.0.0.1:5434/postgres:
['10.13s', '10.13s', '10.14s', '10.14s', '10.14s', '10.14s', '10.14s', '10.14s', '10.14s', '10.14s', '10.14s', '10.14s', '10.14s', '10.14s', '10.14s', '10.14s', '10.14s', '10.14s', '10.14s', '10.14s', '10.14s', '10.14s', '10.14s', '10.14s', '10.14s', '10.14s', '10.14s', '10.14s', '10.14s', '10.14s', '10.14s', '10.14s']
```

There's a lot of logs for the pgbouncer -> cloudsqlproxy case but not for others.

```
pgbouncer-1  | 2024-04-19 14:03:30.749 UTC [1] LOG C-0xffffb537b3c0: cloudsql/postgres@192.168.65.1:24988 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.749 UTC [1] LOG C-0xffffb537b920: cloudsql/postgres@192.168.65.1:24990 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.749 UTC [1] LOG C-0xffffb537b3c0: cloudsql/postgres@192.168.65.1:24988 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.749 UTC [1] LOG C-0xffffb537b920: cloudsql/postgres@192.168.65.1:24990 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537b670: cloudsql/postgres@192.168.65.1:24989 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537c130: cloudsql/postgres@192.168.65.1:24993 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537be80: cloudsql/postgres@192.168.65.1:24992 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537bbd0: cloudsql/postgres@192.168.65.1:24991 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537cea0: cloudsql/postgres@192.168.65.1:24998 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537cbf0: cloudsql/postgres@192.168.65.1:24997 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537c940: cloudsql/postgres@192.168.65.1:24996 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537c690: cloudsql/postgres@192.168.65.1:24994 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537c3e0: cloudsql/postgres@192.168.65.1:24995 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537e170: cloudsql/postgres@192.168.65.1:25004 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537dec0: cloudsql/postgres@192.168.65.1:25005 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537d960: cloudsql/postgres@192.168.65.1:25003 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537d6b0: cloudsql/postgres@192.168.65.1:25001 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537b670: cloudsql/postgres@192.168.65.1:24989 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537c130: cloudsql/postgres@192.168.65.1:24993 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537be80: cloudsql/postgres@192.168.65.1:24992 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537bbd0: cloudsql/postgres@192.168.65.1:24991 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537cea0: cloudsql/postgres@192.168.65.1:24998 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537cbf0: cloudsql/postgres@192.168.65.1:24997 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537c940: cloudsql/postgres@192.168.65.1:24996 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537c690: cloudsql/postgres@192.168.65.1:24994 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537c3e0: cloudsql/postgres@192.168.65.1:24995 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537e170: cloudsql/postgres@192.168.65.1:25004 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537dec0: cloudsql/postgres@192.168.65.1:25005 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537d960: cloudsql/postgres@192.168.65.1:25003 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537d6b0: cloudsql/postgres@192.168.65.1:25001 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537dc10: cloudsql/postgres@192.168.65.1:25002 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537e980: cloudsql/postgres@192.168.65.1:25008 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537d400: cloudsql/postgres@192.168.65.1:25000 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537d150: cloudsql/postgres@192.168.65.1:24999 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537e6d0: cloudsql/postgres@192.168.65.1:25007 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537f440: cloudsql/postgres@192.168.65.1:25009 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537e420: cloudsql/postgres@192.168.65.1:25006 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537f6f0: cloudsql/postgres@192.168.65.1:25013 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.751 UTC [1] LOG C-0xffffb537f190: cloudsql/postgres@192.168.65.1:25012 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.751 UTC [1] LOG C-0xffffb537eee0: cloudsql/postgres@192.168.65.1:25011 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.751 UTC [1] LOG C-0xffffb537ec30: cloudsql/postgres@192.168.65.1:25010 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.751 UTC [1] LOG C-0xffffb53801b0: cloudsql/postgres@192.168.65.1:25017 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.751 UTC [1] LOG C-0xffffb537ff00: cloudsql/postgres@192.168.65.1:25016 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.751 UTC [1] LOG C-0xffffb537fc50: cloudsql/postgres@192.168.65.1:25015 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.751 UTC [1] LOG C-0xffffb537f9a0: cloudsql/postgres@192.168.65.1:25014 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.751 UTC [1] LOG C-0xffffb5380710: cloudsql/postgres@192.168.65.1:25019 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.751 UTC [1] LOG C-0xffffb5380460: cloudsql/postgres@192.168.65.1:25018 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537dc10: cloudsql/postgres@192.168.65.1:25002 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537e980: cloudsql/postgres@192.168.65.1:25008 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537d400: cloudsql/postgres@192.168.65.1:25000 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537d150: cloudsql/postgres@192.168.65.1:24999 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537e6d0: cloudsql/postgres@192.168.65.1:25007 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537f440: cloudsql/postgres@192.168.65.1:25009 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537e420: cloudsql/postgres@192.168.65.1:25006 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.750 UTC [1] LOG C-0xffffb537f6f0: cloudsql/postgres@192.168.65.1:25013 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.751 UTC [1] LOG C-0xffffb537f190: cloudsql/postgres@192.168.65.1:25012 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.751 UTC [1] LOG C-0xffffb537eee0: cloudsql/postgres@192.168.65.1:25011 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.751 UTC [1] LOG C-0xffffb537ec30: cloudsql/postgres@192.168.65.1:25010 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.751 UTC [1] LOG C-0xffffb53801b0: cloudsql/postgres@192.168.65.1:25017 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.751 UTC [1] LOG C-0xffffb537ff00: cloudsql/postgres@192.168.65.1:25016 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.751 UTC [1] LOG C-0xffffb537fc50: cloudsql/postgres@192.168.65.1:25015 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.751 UTC [1] LOG C-0xffffb537f9a0: cloudsql/postgres@192.168.65.1:25014 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.751 UTC [1] LOG C-0xffffb5380710: cloudsql/postgres@192.168.65.1:25019 login attempt: db=cloudsql user=postgres tls=no
pgbouncer-1  | 2024-04-19 14:03:30.751 UTC [1] LOG C-0xffffb5380460: cloudsql/postgres@192.168.65.1:25018 login attempt: db=cloudsql user=postgres tls=no
cloudql-1    | 2024/04/19 14:03:30 [<instance-name>] Accepted connection from 172.22.0.3:51144
cloudql-1    | 2024/04/19 14:03:30 [<instance-name>] Now = 2024-04-19T14:03:30Z, Current cert expiration = 2024-04-19T15:03:29Z
pgbouncer-1  | 2024-04-19 14:03:30.879 UTC [1] LOG S-0xffffb53203f0: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:51144)
pgbouncer-1  | 2024-04-19 14:03:30.879 UTC [1] LOG S-0xffffb53203f0: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:51144)
cloudql-1    | 2024/04/19 14:03:30 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:30 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:03:31.181 UTC [1] LOG S-0xffffb53206a0: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:51152)
pgbouncer-1  | 2024-04-19 14:03:31.181 UTC [1] LOG S-0xffffb53206a0: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:51152)
cloudql-1    | 2024/04/19 14:03:31 [<instance-name>] Accepted connection from 172.22.0.3:51152
cloudql-1    | 2024/04/19 14:03:31 [<instance-name>] Now = 2024-04-19T14:03:31Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:31 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:31 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:03:31.458 UTC [1] LOG S-0xffffb5320950: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:51160)
pgbouncer-1  | 2024-04-19 14:03:31.458 UTC [1] LOG S-0xffffb5320950: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:51160)
cloudql-1    | 2024/04/19 14:03:31 [<instance-name>] Accepted connection from 172.22.0.3:51160
cloudql-1    | 2024/04/19 14:03:31 [<instance-name>] Now = 2024-04-19T14:03:31Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:31 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:31 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:31 [<instance-name>] Accepted connection from 172.22.0.3:51162
cloudql-1    | 2024/04/19 14:03:31 [<instance-name>] Now = 2024-04-19T14:03:31Z, Current cert expiration = 2024-04-19T15:03:29Z
pgbouncer-1  | 2024-04-19 14:03:31.732 UTC [1] LOG S-0xffffb5320c00: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:51162)
pgbouncer-1  | 2024-04-19 14:03:31.732 UTC [1] LOG S-0xffffb5320c00: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:51162)
cloudql-1    | 2024/04/19 14:03:31 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:31 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:32 [<instance-name>] Accepted connection from 172.22.0.3:51172
cloudql-1    | 2024/04/19 14:03:32 [<instance-name>] Now = 2024-04-19T14:03:32Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:32 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:32 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:03:32.021 UTC [1] LOG S-0xffffb5320eb0: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:51172)
pgbouncer-1  | 2024-04-19 14:03:32.021 UTC [1] LOG S-0xffffb5320eb0: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:51172)
pgbouncer-1  | 2024-04-19 14:03:32.281 UTC [1] LOG S-0xffffb5321160: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:51188)
cloudql-1    | 2024/04/19 14:03:32 [<instance-name>] Accepted connection from 172.22.0.3:51188
pgbouncer-1  | 2024-04-19 14:03:32.281 UTC [1] LOG S-0xffffb5321160: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:51188)
cloudql-1    | 2024/04/19 14:03:32 [<instance-name>] Now = 2024-04-19T14:03:32Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:32 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:32 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:03:32.579 UTC [1] LOG S-0xffffb5321410: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:51202)
pgbouncer-1  | 2024-04-19 14:03:32.579 UTC [1] LOG S-0xffffb5321410: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:51202)
cloudql-1    | 2024/04/19 14:03:32 [<instance-name>] Accepted connection from 172.22.0.3:51202
cloudql-1    | 2024/04/19 14:03:32 [<instance-name>] Now = 2024-04-19T14:03:32Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:32 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:32 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:32 [<instance-name>] Accepted connection from 172.22.0.3:51218
cloudql-1    | 2024/04/19 14:03:32 [<instance-name>] Now = 2024-04-19T14:03:32Z, Current cert expiration = 2024-04-19T15:03:29Z
pgbouncer-1  | 2024-04-19 14:03:32.858 UTC [1] LOG S-0xffffb53216c0: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:51218)
pgbouncer-1  | 2024-04-19 14:03:32.858 UTC [1] LOG S-0xffffb53216c0: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:51218)
cloudql-1    | 2024/04/19 14:03:32 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:32 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:33 [<instance-name>] Accepted connection from 172.22.0.3:51228
cloudql-1    | 2024/04/19 14:03:33 [<instance-name>] Now = 2024-04-19T14:03:33Z, Current cert expiration = 2024-04-19T15:03:29Z
pgbouncer-1  | 2024-04-19 14:03:33.122 UTC [1] LOG S-0xffffb5321970: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:51228)
pgbouncer-1  | 2024-04-19 14:03:33.122 UTC [1] LOG S-0xffffb5321970: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:51228)
cloudql-1    | 2024/04/19 14:03:33 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:33 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:33 [<instance-name>] Accepted connection from 172.22.0.3:51238
cloudql-1    | 2024/04/19 14:03:33 [<instance-name>] Now = 2024-04-19T14:03:33Z, Current cert expiration = 2024-04-19T15:03:29Z
pgbouncer-1  | 2024-04-19 14:03:33.413 UTC [1] LOG S-0xffffb5321c20: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:51238)
pgbouncer-1  | 2024-04-19 14:03:33.413 UTC [1] LOG S-0xffffb5321c20: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:51238)
cloudql-1    | 2024/04/19 14:03:33 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:33 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:33 [<instance-name>] Accepted connection from 172.22.0.3:51250
cloudql-1    | 2024/04/19 14:03:33 [<instance-name>] Now = 2024-04-19T14:03:33Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:33 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:33 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:03:33.696 UTC [1] LOG S-0xffffb5321ed0: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:51250)
pgbouncer-1  | 2024-04-19 14:03:33.696 UTC [1] LOG S-0xffffb5321ed0: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:51250)
pgbouncer-1  | 2024-04-19 14:03:34.979 UTC [1] LOG S-0xffffb5322180: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:51260)
pgbouncer-1  | 2024-04-19 14:03:34.979 UTC [1] LOG S-0xffffb5322180: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:51260)
cloudql-1    | 2024/04/19 14:03:34 [<instance-name>] Accepted connection from 172.22.0.3:51260
cloudql-1    | 2024/04/19 14:03:34 [<instance-name>] Now = 2024-04-19T14:03:34Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:34 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:34 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:35 [<instance-name>] Accepted connection from 172.22.0.3:51264
cloudql-1    | 2024/04/19 14:03:35 [<instance-name>] Now = 2024-04-19T14:03:35Z, Current cert expiration = 2024-04-19T15:03:29Z
pgbouncer-1  | 2024-04-19 14:03:35.253 UTC [1] LOG S-0xffffb5322430: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:51264)
pgbouncer-1  | 2024-04-19 14:03:35.253 UTC [1] LOG S-0xffffb5322430: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:51264)
cloudql-1    | 2024/04/19 14:03:35 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:35 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:03:35.561 UTC [1] LOG S-0xffffb53226e0: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:51276)
pgbouncer-1  | 2024-04-19 14:03:35.561 UTC [1] LOG S-0xffffb53226e0: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:51276)
cloudql-1    | 2024/04/19 14:03:35 [<instance-name>] Accepted connection from 172.22.0.3:51276
cloudql-1    | 2024/04/19 14:03:35 [<instance-name>] Now = 2024-04-19T14:03:35Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:35 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:35 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:03:35.862 UTC [1] LOG S-0xffffb5322990: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:51292)
pgbouncer-1  | 2024-04-19 14:03:35.862 UTC [1] LOG S-0xffffb5322990: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:51292)
cloudql-1    | 2024/04/19 14:03:35 [<instance-name>] Accepted connection from 172.22.0.3:51292
cloudql-1    | 2024/04/19 14:03:35 [<instance-name>] Now = 2024-04-19T14:03:35Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:35 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:35 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:03:36.137 UTC [1] LOG S-0xffffb5322c40: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:51294)
pgbouncer-1  | 2024-04-19 14:03:36.137 UTC [1] LOG S-0xffffb5322c40: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:51294)
cloudql-1    | 2024/04/19 14:03:36 [<instance-name>] Accepted connection from 172.22.0.3:51294
cloudql-1    | 2024/04/19 14:03:36 [<instance-name>] Now = 2024-04-19T14:03:36Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:36 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:36 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:03:36.416 UTC [1] LOG S-0xffffb5322ef0: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:51308)
pgbouncer-1  | 2024-04-19 14:03:36.416 UTC [1] LOG S-0xffffb5322ef0: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:51308)
cloudql-1    | 2024/04/19 14:03:36 [<instance-name>] Accepted connection from 172.22.0.3:51308
cloudql-1    | 2024/04/19 14:03:36 [<instance-name>] Now = 2024-04-19T14:03:36Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:36 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:36 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:36 [<instance-name>] Accepted connection from 172.22.0.3:50768
cloudql-1    | 2024/04/19 14:03:36 [<instance-name>] Now = 2024-04-19T14:03:36Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:36 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:36 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:03:36.681 UTC [1] LOG S-0xffffb53231a0: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:50768)
pgbouncer-1  | 2024-04-19 14:03:36.681 UTC [1] LOG S-0xffffb53231a0: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:50768)
pgbouncer-1  | 2024-04-19 14:03:36.983 UTC [1] LOG S-0xffffb5323450: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:50774)
pgbouncer-1  | 2024-04-19 14:03:36.983 UTC [1] LOG S-0xffffb5323450: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:50774)
cloudql-1    | 2024/04/19 14:03:36 [<instance-name>] Accepted connection from 172.22.0.3:50774
cloudql-1    | 2024/04/19 14:03:36 [<instance-name>] Now = 2024-04-19T14:03:36Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:36 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:36 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:37 [<instance-name>] Accepted connection from 172.22.0.3:50790
cloudql-1    | 2024/04/19 14:03:37 [<instance-name>] Now = 2024-04-19T14:03:37Z, Current cert expiration = 2024-04-19T15:03:29Z
pgbouncer-1  | 2024-04-19 14:03:37.263 UTC [1] LOG S-0xffffb5323700: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:50790)
pgbouncer-1  | 2024-04-19 14:03:37.263 UTC [1] LOG S-0xffffb5323700: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:50790)
cloudql-1    | 2024/04/19 14:03:37 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:37 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:03:37.512 UTC [1] LOG S-0xffffb53239b0: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:50802)
pgbouncer-1  | 2024-04-19 14:03:37.512 UTC [1] LOG S-0xffffb53239b0: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:50802)
cloudql-1    | 2024/04/19 14:03:37 [<instance-name>] Accepted connection from 172.22.0.3:50802
cloudql-1    | 2024/04/19 14:03:37 [<instance-name>] Now = 2024-04-19T14:03:37Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:37 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:37 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:03:37.820 UTC [1] LOG S-0xffffb5323c60: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:50810)
pgbouncer-1  | 2024-04-19 14:03:37.820 UTC [1] LOG S-0xffffb5323c60: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:50810)
cloudql-1    | 2024/04/19 14:03:37 [<instance-name>] Accepted connection from 172.22.0.3:50810
cloudql-1    | 2024/04/19 14:03:37 [<instance-name>] Now = 2024-04-19T14:03:37Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:37 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:37 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:38 [<instance-name>] Accepted connection from 172.22.0.3:50824
cloudql-1    | 2024/04/19 14:03:38 [<instance-name>] Now = 2024-04-19T14:03:38Z, Current cert expiration = 2024-04-19T15:03:29Z
pgbouncer-1  | 2024-04-19 14:03:38.092 UTC [1] LOG S-0xffffb5323f10: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:50824)
pgbouncer-1  | 2024-04-19 14:03:38.092 UTC [1] LOG S-0xffffb5323f10: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:50824)
cloudql-1    | 2024/04/19 14:03:38 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:38 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:03:38.378 UTC [1] LOG S-0xffffb53241c0: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:50838)
pgbouncer-1  | 2024-04-19 14:03:38.378 UTC [1] LOG S-0xffffb53241c0: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:50838)
cloudql-1    | 2024/04/19 14:03:38 [<instance-name>] Accepted connection from 172.22.0.3:50838
cloudql-1    | 2024/04/19 14:03:38 [<instance-name>] Now = 2024-04-19T14:03:38Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:38 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:38 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:38 [<instance-name>] Accepted connection from 172.22.0.3:50852
cloudql-1    | 2024/04/19 14:03:38 [<instance-name>] Now = 2024-04-19T14:03:38Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:38 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:38 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:03:38.658 UTC [1] LOG S-0xffffb5324470: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:50852)
pgbouncer-1  | 2024-04-19 14:03:38.658 UTC [1] LOG S-0xffffb5324470: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:50852)
cloudql-1    | 2024/04/19 14:03:38 [<instance-name>] Accepted connection from 172.22.0.3:50864
cloudql-1    | 2024/04/19 14:03:38 [<instance-name>] Now = 2024-04-19T14:03:38Z, Current cert expiration = 2024-04-19T15:03:29Z
pgbouncer-1  | 2024-04-19 14:03:38.936 UTC [1] LOG S-0xffffb5324720: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:50864)
pgbouncer-1  | 2024-04-19 14:03:38.936 UTC [1] LOG S-0xffffb5324720: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:50864)
cloudql-1    | 2024/04/19 14:03:38 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:38 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:39 [<instance-name>] Accepted connection from 172.22.0.3:50880
cloudql-1    | 2024/04/19 14:03:39 [<instance-name>] Now = 2024-04-19T14:03:39Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:39 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:39 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:03:39.203 UTC [1] LOG S-0xffffb53249d0: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:50880)
pgbouncer-1  | 2024-04-19 14:03:39.203 UTC [1] LOG S-0xffffb53249d0: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:50880)
pgbouncer-1  | 2024-04-19 14:03:39.478 UTC [1] LOG S-0xffffb5324c80: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:50890)
pgbouncer-1  | 2024-04-19 14:03:39.478 UTC [1] LOG S-0xffffb5324c80: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:50890)
cloudql-1    | 2024/04/19 14:03:39 [<instance-name>] Accepted connection from 172.22.0.3:50890
cloudql-1    | 2024/04/19 14:03:39 [<instance-name>] Now = 2024-04-19T14:03:39Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:39 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:39 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:39 [<instance-name>] Accepted connection from 172.22.0.3:50898
cloudql-1    | 2024/04/19 14:03:39 [<instance-name>] Now = 2024-04-19T14:03:39Z, Current cert expiration = 2024-04-19T15:03:29Z
pgbouncer-1  | 2024-04-19 14:03:39.760 UTC [1] LOG S-0xffffb5324f30: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:50898)
pgbouncer-1  | 2024-04-19 14:03:39.760 UTC [1] LOG S-0xffffb5324f30: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:50898)
cloudql-1    | 2024/04/19 14:03:39 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:39 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:03:40.017 UTC [1] LOG S-0xffffb53251e0: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:50906)
cloudql-1    | 2024/04/19 14:03:40 [<instance-name>] Accepted connection from 172.22.0.3:50906
pgbouncer-1  | 2024-04-19 14:03:40.017 UTC [1] LOG S-0xffffb53251e0: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:50906)
cloudql-1    | 2024/04/19 14:03:40 [<instance-name>] Now = 2024-04-19T14:03:40Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:40 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:40 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:03:40.296 UTC [1] LOG S-0xffffb5325490: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:50910)
pgbouncer-1  | 2024-04-19 14:03:40.296 UTC [1] LOG S-0xffffb5325490: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:50910)
cloudql-1    | 2024/04/19 14:03:40 [<instance-name>] Accepted connection from 172.22.0.3:50910
cloudql-1    | 2024/04/19 14:03:40 [<instance-name>] Now = 2024-04-19T14:03:40Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:40 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:40 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:40 [<instance-name>] Accepted connection from 172.22.0.3:50914
cloudql-1    | 2024/04/19 14:03:40 [<instance-name>] Now = 2024-04-19T14:03:40Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:40 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:40 [<instance-name>] Dialing 34.70.74.26:3307
pgbouncer-1  | 2024-04-19 14:03:40.576 UTC [1] LOG S-0xffffb5325740: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:50914)
pgbouncer-1  | 2024-04-19 14:03:40.576 UTC [1] LOG S-0xffffb5325740: cloudsql/postgres@172.22.0.4:5432 new connection to server (from 172.22.0.3:50914)
pgbouncer-1  | 2024-04-19 14:03:41.568 UTC [1] LOG C-0xffffb537b920: cloudsql/postgres@192.168.65.1:24990 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:03:41.568 UTC [1] LOG S-0xffffb53203f0: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:03:41.568 UTC [1] LOG C-0xffffb537b920: cloudsql/postgres@192.168.65.1:24990 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:03:41.568 UTC [1] LOG S-0xffffb53203f0: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:03:41 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:03:41 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:03:41.575 UTC [1] LOG C-0xffffb537f6f0: cloudsql/postgres@192.168.65.1:25013 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:03:41.575 UTC [1] LOG S-0xffffb53206a0: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:03:41.575 UTC [1] LOG C-0xffffb537f6f0: cloudsql/postgres@192.168.65.1:25013 closing because: client close request (age=10s)
pgbouncer-1  | 2024-04-19 14:03:41.575 UTC [1] LOG S-0xffffb53206a0: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:03:41 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:03:41.842 UTC [1] LOG C-0xffffb537e980: cloudsql/postgres@192.168.65.1:25008 closing because: client close request (age=11s)
pgbouncer-1  | 2024-04-19 14:03:41.842 UTC [1] LOG S-0xffffb5320950: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:03:41.842 UTC [1] LOG C-0xffffb537e980: cloudsql/postgres@192.168.65.1:25008 closing because: client close request (age=11s)
pgbouncer-1  | 2024-04-19 14:03:41.842 UTC [1] LOG S-0xffffb5320950: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:03:42.489 UTC [1] LOG C-0xffffb537dc10: cloudsql/postgres@192.168.65.1:25002 closing because: client close request (age=11s)
pgbouncer-1  | 2024-04-19 14:03:42.489 UTC [1] LOG S-0xffffb5320c00: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:03:42 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:03:42.489 UTC [1] LOG C-0xffffb537dc10: cloudsql/postgres@192.168.65.1:25002 closing because: client close request (age=11s)
pgbouncer-1  | 2024-04-19 14:03:42.489 UTC [1] LOG S-0xffffb5320c00: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:03:42 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:03:42.518 UTC [1] LOG C-0xffffb537f440: cloudsql/postgres@192.168.65.1:25009 closing because: client close request (age=11s)
pgbouncer-1  | 2024-04-19 14:03:42.518 UTC [1] LOG S-0xffffb5320eb0: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:03:42.518 UTC [1] LOG C-0xffffb537f440: cloudsql/postgres@192.168.65.1:25009 closing because: client close request (age=11s)
pgbouncer-1  | 2024-04-19 14:03:42.518 UTC [1] LOG S-0xffffb5320eb0: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:03:42 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:03:42.689 UTC [1] LOG C-0xffffb537e6d0: cloudsql/postgres@192.168.65.1:25007 closing because: client close request (age=11s)
pgbouncer-1  | 2024-04-19 14:03:42.689 UTC [1] LOG S-0xffffb5321160: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:03:42.689 UTC [1] LOG C-0xffffb537e6d0: cloudsql/postgres@192.168.65.1:25007 closing because: client close request (age=11s)
pgbouncer-1  | 2024-04-19 14:03:42.689 UTC [1] LOG S-0xffffb5321160: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:03:42.992 UTC [1] LOG C-0xffffb537c690: cloudsql/postgres@192.168.65.1:24994 closing because: client close request (age=12s)
pgbouncer-1  | 2024-04-19 14:03:42.993 UTC [1] LOG S-0xffffb5321410: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:03:42 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:03:42.992 UTC [1] LOG C-0xffffb537c690: cloudsql/postgres@192.168.65.1:24994 closing because: client close request (age=12s)
pgbouncer-1  | 2024-04-19 14:03:42.993 UTC [1] LOG S-0xffffb5321410: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:03:43.316 UTC [1] LOG C-0xffffb537ff00: cloudsql/postgres@192.168.65.1:25016 closing because: client close request (age=12s)
pgbouncer-1  | 2024-04-19 14:03:43.316 UTC [1] LOG S-0xffffb53216c0: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:03:43.316 UTC [1] LOG C-0xffffb537ff00: cloudsql/postgres@192.168.65.1:25016 closing because: client close request (age=12s)
pgbouncer-1  | 2024-04-19 14:03:43.316 UTC [1] LOG S-0xffffb53216c0: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:03:43 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:03:43 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:03:43.608 UTC [1] LOG C-0xffffb537b3c0: cloudsql/postgres@192.168.65.1:24988 closing because: client close request (age=12s)
pgbouncer-1  | 2024-04-19 14:03:43.608 UTC [1] LOG S-0xffffb5321970: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:03:43.608 UTC [1] LOG C-0xffffb537b3c0: cloudsql/postgres@192.168.65.1:24988 closing because: client close request (age=12s)
pgbouncer-1  | 2024-04-19 14:03:43.608 UTC [1] LOG S-0xffffb5321970: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:03:43.793 UTC [1] LOG C-0xffffb537fc50: cloudsql/postgres@192.168.65.1:25015 closing because: client close request (age=13s)
pgbouncer-1  | 2024-04-19 14:03:43.793 UTC [1] LOG S-0xffffb5321c20: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:03:43.793 UTC [1] LOG C-0xffffb537fc50: cloudsql/postgres@192.168.65.1:25015 closing because: client close request (age=13s)
pgbouncer-1  | 2024-04-19 14:03:43.793 UTC [1] LOG S-0xffffb5321c20: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:03:43 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:03:45.090 UTC [1] LOG C-0xffffb537dec0: cloudsql/postgres@192.168.65.1:25005 closing because: client close request (age=14s)
pgbouncer-1  | 2024-04-19 14:03:45.090 UTC [1] LOG S-0xffffb5321ed0: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=11s)
pgbouncer-1  | 2024-04-19 14:03:45.090 UTC [1] LOG C-0xffffb537dec0: cloudsql/postgres@192.168.65.1:25005 closing because: client close request (age=14s)
pgbouncer-1  | 2024-04-19 14:03:45.090 UTC [1] LOG S-0xffffb5321ed0: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=11s)
cloudql-1    | 2024/04/19 14:03:45 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:03:45.379 UTC [1] LOG C-0xffffb537e420: cloudsql/postgres@192.168.65.1:25006 closing because: client close request (age=14s)
pgbouncer-1  | 2024-04-19 14:03:45.379 UTC [1] LOG S-0xffffb5322180: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:03:45.379 UTC [1] LOG C-0xffffb537e420: cloudsql/postgres@192.168.65.1:25006 closing because: client close request (age=14s)
pgbouncer-1  | 2024-04-19 14:03:45.379 UTC [1] LOG S-0xffffb5322180: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:03:45 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:03:45.689 UTC [1] LOG C-0xffffb537d6b0: cloudsql/postgres@192.168.65.1:25001 closing because: client close request (age=14s)
pgbouncer-1  | 2024-04-19 14:03:45.689 UTC [1] LOG S-0xffffb5322430: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:03:45.689 UTC [1] LOG C-0xffffb537d6b0: cloudsql/postgres@192.168.65.1:25001 closing because: client close request (age=14s)
pgbouncer-1  | 2024-04-19 14:03:45.689 UTC [1] LOG S-0xffffb5322430: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:03:45 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:03:45 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:03:45.969 UTC [1] LOG C-0xffffb5380710: cloudsql/postgres@192.168.65.1:25019 closing because: client close request (age=15s)
pgbouncer-1  | 2024-04-19 14:03:45.969 UTC [1] LOG S-0xffffb53226e0: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:03:45.969 UTC [1] LOG C-0xffffb5380710: cloudsql/postgres@192.168.65.1:25019 closing because: client close request (age=15s)
pgbouncer-1  | 2024-04-19 14:03:45.969 UTC [1] LOG S-0xffffb53226e0: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:03:46.255 UTC [1] LOG C-0xffffb537c130: cloudsql/postgres@192.168.65.1:24993 closing because: client close request (age=15s)
pgbouncer-1  | 2024-04-19 14:03:46.255 UTC [1] LOG S-0xffffb5322990: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:03:46.255 UTC [1] LOG C-0xffffb537c130: cloudsql/postgres@192.168.65.1:24993 closing because: client close request (age=15s)
pgbouncer-1  | 2024-04-19 14:03:46.255 UTC [1] LOG S-0xffffb5322990: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:03:46 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:03:46.544 UTC [1] LOG C-0xffffb537cbf0: cloudsql/postgres@192.168.65.1:24997 closing because: client close request (age=15s)
pgbouncer-1  | 2024-04-19 14:03:46.544 UTC [1] LOG S-0xffffb5322c40: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:03:46.544 UTC [1] LOG C-0xffffb537cbf0: cloudsql/postgres@192.168.65.1:24997 closing because: client close request (age=15s)
pgbouncer-1  | 2024-04-19 14:03:46.544 UTC [1] LOG S-0xffffb5322c40: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:03:46 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:03:46.803 UTC [1] LOG C-0xffffb537c3e0: cloudsql/postgres@192.168.65.1:24995 closing because: client close request (age=16s)
pgbouncer-1  | 2024-04-19 14:03:46.803 UTC [1] LOG S-0xffffb5322ef0: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:03:46.803 UTC [1] LOG C-0xffffb537c3e0: cloudsql/postgres@192.168.65.1:24995 closing because: client close request (age=16s)
pgbouncer-1  | 2024-04-19 14:03:46.803 UTC [1] LOG S-0xffffb5322ef0: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:03:46 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:03:47.085 UTC [1] LOG C-0xffffb537bbd0: cloudsql/postgres@192.168.65.1:24991 closing because: client close request (age=16s)
pgbouncer-1  | 2024-04-19 14:03:47.085 UTC [1] LOG S-0xffffb53231a0: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:03:47.085 UTC [1] LOG C-0xffffb537bbd0: cloudsql/postgres@192.168.65.1:24991 closing because: client close request (age=16s)
pgbouncer-1  | 2024-04-19 14:03:47.085 UTC [1] LOG S-0xffffb53231a0: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:03:47 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:03:47.358 UTC [1] LOG C-0xffffb537c940: cloudsql/postgres@192.168.65.1:24996 closing because: client close request (age=16s)
pgbouncer-1  | 2024-04-19 14:03:47.358 UTC [1] LOG S-0xffffb5323450: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:03:47.358 UTC [1] LOG C-0xffffb537c940: cloudsql/postgres@192.168.65.1:24996 closing because: client close request (age=16s)
pgbouncer-1  | 2024-04-19 14:03:47.358 UTC [1] LOG S-0xffffb5323450: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:03:47 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:03:47.709 UTC [1] LOG C-0xffffb537d960: cloudsql/postgres@192.168.65.1:25003 closing because: client close request (age=16s)
pgbouncer-1  | 2024-04-19 14:03:47.709 UTC [1] LOG S-0xffffb5323700: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:03:47.709 UTC [1] LOG C-0xffffb537d960: cloudsql/postgres@192.168.65.1:25003 closing because: client close request (age=16s)
pgbouncer-1  | 2024-04-19 14:03:47.709 UTC [1] LOG S-0xffffb5323700: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:03:47 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:03:47.978 UTC [1] LOG C-0xffffb537d150: cloudsql/postgres@192.168.65.1:24999 closing because: client close request (age=17s)
pgbouncer-1  | 2024-04-19 14:03:47.978 UTC [1] LOG S-0xffffb53239b0: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:03:47.978 UTC [1] LOG C-0xffffb537d150: cloudsql/postgres@192.168.65.1:24999 closing because: client close request (age=17s)
pgbouncer-1  | 2024-04-19 14:03:47.978 UTC [1] LOG S-0xffffb53239b0: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:03:47 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:03:48.566 UTC [1] LOG C-0xffffb537b670: cloudsql/postgres@192.168.65.1:24989 closing because: client close request (age=17s)
pgbouncer-1  | 2024-04-19 14:03:48.566 UTC [1] LOG S-0xffffb5323f10: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:03:48.567 UTC [1] LOG C-0xffffb537eee0: cloudsql/postgres@192.168.65.1:25011 closing because: client close request (age=17s)
pgbouncer-1  | 2024-04-19 14:03:48.567 UTC [1] LOG S-0xffffb5323c60: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:03:48.566 UTC [1] LOG C-0xffffb537b670: cloudsql/postgres@192.168.65.1:24989 closing because: client close request (age=17s)
pgbouncer-1  | 2024-04-19 14:03:48.566 UTC [1] LOG S-0xffffb5323f10: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:03:48.567 UTC [1] LOG C-0xffffb537eee0: cloudsql/postgres@192.168.65.1:25011 closing because: client close request (age=17s)
pgbouncer-1  | 2024-04-19 14:03:48.567 UTC [1] LOG S-0xffffb5323c60: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:03:48 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:03:48 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:03:48.774 UTC [1] LOG C-0xffffb537ec30: cloudsql/postgres@192.168.65.1:25010 closing because: client close request (age=18s)
pgbouncer-1  | 2024-04-19 14:03:48.774 UTC [1] LOG S-0xffffb53241c0: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:03:48 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:03:48.774 UTC [1] LOG C-0xffffb537ec30: cloudsql/postgres@192.168.65.1:25010 closing because: client close request (age=18s)
pgbouncer-1  | 2024-04-19 14:03:48.774 UTC [1] LOG S-0xffffb53241c0: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:03:49.061 UTC [1] LOG C-0xffffb53801b0: cloudsql/postgres@192.168.65.1:25017 closing because: client close request (age=18s)
pgbouncer-1  | 2024-04-19 14:03:49.062 UTC [1] LOG S-0xffffb5324470: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:03:49.061 UTC [1] LOG C-0xffffb53801b0: cloudsql/postgres@192.168.65.1:25017 closing because: client close request (age=18s)
pgbouncer-1  | 2024-04-19 14:03:49.062 UTC [1] LOG S-0xffffb5324470: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:03:49 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:03:49.301 UTC [1] LOG C-0xffffb5380460: cloudsql/postgres@192.168.65.1:25018 closing because: client close request (age=18s)
pgbouncer-1  | 2024-04-19 14:03:49.301 UTC [1] LOG S-0xffffb5324720: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:03:49.301 UTC [1] LOG C-0xffffb5380460: cloudsql/postgres@192.168.65.1:25018 closing because: client close request (age=18s)
pgbouncer-1  | 2024-04-19 14:03:49.301 UTC [1] LOG S-0xffffb5324720: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:03:49 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:03:49 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:03:49.583 UTC [1] LOG C-0xffffb537d400: cloudsql/postgres@192.168.65.1:25000 closing because: client close request (age=18s)
pgbouncer-1  | 2024-04-19 14:03:49.583 UTC [1] LOG S-0xffffb53249d0: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:03:49.583 UTC [1] LOG C-0xffffb537d400: cloudsql/postgres@192.168.65.1:25000 closing because: client close request (age=18s)
pgbouncer-1  | 2024-04-19 14:03:49.583 UTC [1] LOG S-0xffffb53249d0: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:03:49.869 UTC [1] LOG C-0xffffb537f190: cloudsql/postgres@192.168.65.1:25012 closing because: client close request (age=19s)
pgbouncer-1  | 2024-04-19 14:03:49.869 UTC [1] LOG S-0xffffb5324c80: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:03:49.869 UTC [1] LOG C-0xffffb537f190: cloudsql/postgres@192.168.65.1:25012 closing because: client close request (age=19s)
pgbouncer-1  | 2024-04-19 14:03:49.869 UTC [1] LOG S-0xffffb5324c80: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:03:49 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:03:50.479 UTC [1] LOG C-0xffffb537be80: cloudsql/postgres@192.168.65.1:24992 closing because: client close request (age=19s)
pgbouncer-1  | 2024-04-19 14:03:50.479 UTC [1] LOG S-0xffffb5324f30: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:03:50.479 UTC [1] LOG C-0xffffb537f9a0: cloudsql/postgres@192.168.65.1:25014 closing because: client close request (age=19s)
pgbouncer-1  | 2024-04-19 14:03:50.479 UTC [1] LOG S-0xffffb53251e0: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:03:50.479 UTC [1] LOG C-0xffffb537be80: cloudsql/postgres@192.168.65.1:24992 closing because: client close request (age=19s)
pgbouncer-1  | 2024-04-19 14:03:50.479 UTC [1] LOG S-0xffffb5324f30: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:03:50.479 UTC [1] LOG C-0xffffb537f9a0: cloudsql/postgres@192.168.65.1:25014 closing because: client close request (age=19s)
pgbouncer-1  | 2024-04-19 14:03:50.479 UTC [1] LOG S-0xffffb53251e0: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:03:50 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:03:50 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:03:50.684 UTC [1] LOG C-0xffffb537e170: cloudsql/postgres@192.168.65.1:25004 closing because: client close request (age=19s)
pgbouncer-1  | 2024-04-19 14:03:50.684 UTC [1] LOG S-0xffffb5325490: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:03:50.684 UTC [1] LOG C-0xffffb537e170: cloudsql/postgres@192.168.65.1:25004 closing because: client close request (age=19s)
pgbouncer-1  | 2024-04-19 14:03:50.684 UTC [1] LOG S-0xffffb5325490: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:03:50 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:03:51.056 UTC [1] LOG C-0xffffb537cea0: cloudsql/postgres@192.168.65.1:24998 closing because: client close request (age=20s)
pgbouncer-1  | 2024-04-19 14:03:51.056 UTC [1] LOG S-0xffffb5325740: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
pgbouncer-1  | 2024-04-19 14:03:51.056 UTC [1] LOG C-0xffffb537cea0: cloudsql/postgres@192.168.65.1:24998 closing because: client close request (age=20s)
pgbouncer-1  | 2024-04-19 14:03:51.056 UTC [1] LOG S-0xffffb5325740: cloudsql/postgres@172.22.0.4:5432 closing because: client disconnect while server was not ready (age=10s)
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Accepted connection from 192.168.65.1:37100
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Now = 2024-04-19T14:03:51Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Accepted connection from 192.168.65.1:37089
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Accepted connection from 192.168.65.1:37085
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Accepted connection from 192.168.65.1:37090
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Accepted connection from 192.168.65.1:37094
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Accepted connection from 192.168.65.1:37103
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Accepted connection from 192.168.65.1:37078
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Now = 2024-04-19T14:03:51Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Accepted connection from 192.168.65.1:37104
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Accepted connection from 192.168.65.1:37092
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Now = 2024-04-19T14:03:51Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Now = 2024-04-19T14:03:51Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Accepted connection from 192.168.65.1:37079
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Now = 2024-04-19T14:03:51Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Now = 2024-04-19T14:03:51Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Now = 2024-04-19T14:03:51Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Accepted connection from 192.168.65.1:37105
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Now = 2024-04-19T14:03:51Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Now = 2024-04-19T14:03:51Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Accepted connection from 192.168.65.1:37096
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Now = 2024-04-19T14:03:51Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Accepted connection from 192.168.65.1:37102
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Now = 2024-04-19T14:03:51Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Now = 2024-04-19T14:03:51Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Accepted connection from 192.168.65.1:37095
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Now = 2024-04-19T14:03:51Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Now = 2024-04-19T14:03:51Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Accepted connection from 192.168.65.1:37101
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Now = 2024-04-19T14:03:51Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Accepted connection from 192.168.65.1:37097
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Now = 2024-04-19T14:03:51Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Accepted connection from 192.168.65.1:37098
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Now = 2024-04-19T14:03:51Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Accepted connection from 192.168.65.1:37099
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Now = 2024-04-19T14:03:51Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Accepted connection from 192.168.65.1:37080
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Now = 2024-04-19T14:03:51Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Accepted connection from 192.168.65.1:37081
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Now = 2024-04-19T14:03:51Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Accepted connection from 192.168.65.1:37082
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Now = 2024-04-19T14:03:51Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Accepted connection from 192.168.65.1:37083
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Now = 2024-04-19T14:03:51Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Accepted connection from 192.168.65.1:37088
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Now = 2024-04-19T14:03:51Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Accepted connection from 192.168.65.1:37091
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Now = 2024-04-19T14:03:51Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Accepted connection from 192.168.65.1:37093
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Now = 2024-04-19T14:03:51Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Accepted connection from 192.168.65.1:37084
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Now = 2024-04-19T14:03:51Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Accepted connection from 192.168.65.1:37086
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Now = 2024-04-19T14:03:51Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Accepted connection from 192.168.65.1:37087
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Now = 2024-04-19T14:03:51Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Accepted connection from 192.168.65.1:37107
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Now = 2024-04-19T14:03:51Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Accepted connection from 192.168.65.1:37109
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Now = 2024-04-19T14:03:51Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Accepted connection from 192.168.65.1:37108
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Now = 2024-04-19T14:03:51Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Accepted connection from 192.168.65.1:37106
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Now = 2024-04-19T14:03:51Z, Current cert expiration = 2024-04-19T15:03:29Z
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Cert is valid = true
cloudql-1    | 2024/04/19 14:03:51 [<instance-name>] Dialing 34.70.74.26:3307
cloudql-1    | 2024/04/19 14:04:01 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:04:01 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:04:01 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:04:01 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:04:01 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:04:01 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:04:01 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:04:01 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:04:01 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:04:01 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:04:01 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:04:01 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:04:01 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:04:01 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:04:01 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:04:01 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:04:01 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:04:01 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:04:01 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:04:01 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:04:01 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:04:01 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:04:01 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:04:01 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:04:01 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:04:01 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:04:01 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:04:01 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:04:01 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:04:01 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:04:01 [<instance-name>] client closed the connection
cloudql-1    | 2024/04/19 14:04:01 [<instance-name>] client closed the connection
pgbouncer-1  | 2024-04-19 14:04:28.360 UTC [1] LOG stats: 0 xacts/s, 1 queries/s, 0 client parses/s, 0 server parses/s, 0 binds/s, in 40 B/s, out 51 B/s, xact 0 us, query 7606406 us, wait 2853507 us
pgbouncer-1  | 2024-04-19 14:04:28.360 UTC [1] LOG stats: 0 xacts/s, 1 queries/s, 0 client parses/s, 0 server parses/s, 0 binds/s, in 40 B/s, out 51 B/s, xact 0 us, query 7606406 us, wait 2853507 us
```
