# Eramba CE Docker Install — Walkthrough

**Date:** 22 June 2026
**Host:** macOS 26.3.1, Docker Desktop 29.3.1
**Working dir:** `~/eramba/` (cloned from `github.com/eramba/docker`)
**Access URL:** `https://localhost:8443` (self-signed cert, click through the warning)

## Why this exact stack

Eramba's official install path is a 5-service Docker Compose stack published at
[`github.com/eramba/docker`](https://github.com/eramba/docker). The README is
intentionally thin and points users to Eramba's video learning platform. The
canonical install files are:

| File | Purpose |
|---|---|
| `docker-compose.simple-install.yml` | The 5-service stack (mysql, redis, eramba, cron, triggers_caddy). Rename to `docker-compose.yml`. |
| `.env` | DB credentials, cache URL, public address, secrets. Defaults work out-of-the-box. |
| `apache/ssl/mycert.{crt,key}` | Bundled local-dev certificate. Self-signed. Replace before any real deployment. |

The enterprise variant `docker-compose.simple-install.enterprise.yml` only differs
in image name (`ghcr.io/eramba/eramba-enterprise:latest`). We do not use it.

## Step-by-step

### 1. Verify Docker

```bash
docker --version
# Docker version 29.3.1, build c2be9cc

docker info
# If daemon not running: open -a Docker, wait ~3s, retry.
```

### 2. Clone the repo and prep the working dir

```bash
mkdir -p ~/eramba
cd ~/eramba
git clone --depth 1 https://github.com/eramba/docker.git .
mv docker-compose.simple-install.yml docker-compose.yml
ls -la
```

Expected output: `.env`, `docker-compose.yml`, `apache/`, `crontab/`, `mysql/`,
`php/`, plus README and `.github/`.

### 3. Check ports

```bash
lsof -i :8443 -P -n
```

If 8443 is free (it usually is), proceed. If something else has it, edit `.env`
(`PUBLIC_ADDRESS=https://localhost:8443`) and `docker-compose.yml` (the `ports:
- 8443:443` line under the `eramba` service).

### 4. Bring it up

```bash
docker compose up -d
```

First boot pulls 4 images (mysql, redis, eramba, eramba-triggers). Total pull
~3.5 GB on disk. Then runs 60 database migrations (~35s), seeds defaults, starts
Apache on port 8443.

### 5. Verify

```bash
docker ps
# expect 5 containers: cron, triggers_caddy, eramba, mysql, redis

curl -sk -o /dev/null -w '%{http_code}\n' https://localhost:8443/login
# expect: 200
```

### 6. Open in browser

```bash
open https://localhost:8443
```

Click through the SSL warning (cert is self-signed, expected). Sign in with
`admin` / `admin`. **Force-change the password on first login.**

## What we observed on first boot

```
2026-06-22T23:09 UTC — All Done. Took 34.1659s (60 migrations)
2026-06-22T23:09 UTC — Running third party plugin migrations.
2026-06-22T23:09 UTC — Running InitialSeed to fill in defaults into database.
2026-06-22T23:09 UTC — All done.
2026-06-22T23:10 UTC — Apache/2.4.67 (Debian) PHP/8.4.21 OpenSSL/3.5.6 configured
2026-06-22T23:10 UTC — GET / HTTP/1.1 302 2471 (redirect to /login)
2026-06-22T23:10 UTC — GET /login?redirect=%2F HTTP/1.1 200 5442 (login page rendered)
```

## Known cosmetic warnings (safe to ignore)

```
AH01909: 172.19.0.4:443:0 server certificate does NOT include an ID which matches the server name
```

The bundled `apache/ssl/mycert.crt` is signed for `localhost`-style dev usage; it
does not match the container's internal hostname (`172.19.0.4`). Apache logs this
on every boot. Browsers will warn on first visit. **No security impact for
localhost-only use.** Replace the cert before exposing externally.

## Disk impact

| Image | Size on disk |
|---|---|
| ghcr.io/eramba/eramba:latest | 2.39 GB |
| mysql:8.4.3-oracle | 834 MB |
| ghcr.io/eramba/eramba-triggers:latest | 297 MB |
| redis:7.4.2-alpine | 62 MB |
| **Total** | **~3.6 GB** |

Plus named volumes for db, app data, logs, trigger storage (auto-managed).

## Teardown

```bash
# Stop containers, keep data volumes
cd ~/eramba && docker compose down

# Stop AND wipe all data (fresh re-install next time)
cd ~/eramba && docker compose down -v
```

## Troubleshooting quick reference

| Symptom | Likely cause | Fix |
|---|---|---|
| `Cannot connect to the Docker daemon` | Docker Desktop not running | `open -a Docker`, wait ~3s |
| `Bind for 0.0.0.0:8443 failed: port already allocated` | Port in use by another service | `lsof -i :8443 -P -n` then change `.env` + compose |
| Login page returns 200 but form fields not visible | Browser cached old JS bundle | Hard refresh (Cmd+Shift+R) |
| `502 Bad Gateway` after first boot | MySQL not ready yet, Apache hit before migrations finished | Wait 60-90s, refresh |
| `License check failed` on a gated module | You're on CE, that module is Enterprise-only | See `docs/02-enterprise-gates.md` |
