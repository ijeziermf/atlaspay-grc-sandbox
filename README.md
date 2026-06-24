# atlaspay-grc-sandbox

> A live, running **CISO Assistant Community Edition** instance configured
> with the **AtlasPay** FinTech persona (50 employees, FinTech / payment
> processing industry, SOC 2 framework).
> Companion to
> [helix-health-grc-sandbox](https://github.com/ijeziermf/helix-health-grc-sandbox)
> (HealthTech) and
> [meridian-bank-grc-sandbox](https://github.com/ijeziermf/meridian-bank-grc-sandbox)
> (community bank). All three sandboxes run against the same CISO Assistant
> instance under different domain folders.

## What this repo is

A complete end-to-end GRC ingestion of the AtlasPay FinTech persona into
CISO Assistant, with code, data, scripts, and screenshots. Intended as a
**reproducible reference** for GRC consultants working with FinTech /
payment-processing clients on SOC 2 readiness.

The sandbox contains:

- 1 **folder** (AtlasPay)
- 7 **vendors** (Cloud Provider, Payment Gateway, Identity Provider, Application Platform, Monitoring Tools, Finance Systems, Data Warehouse)
- 7 **contracts** (Master Service Agreements, one per vendor)
- 6 **risk scenarios** with inherent/current/residual risk levels
- 4 **policies** under the Compliance folder (Access Control, Incident Response, Security Awareness, TPRM)
- Multiple **incidents** documented for tabletop exercise reference
- Multiple **assets** and **BCPs** ingested

## History

This repo was originally built against Eramba Community Edition (see
[`docs/00-setup.md`](docs/00-setup.md) for the historical Eramba setup
notes). The current implementation was migrated to CISO Assistant
Community Edition v3.18.3 in 2026-Q2 because CISO Assistant:

- Has a Python/Django ORM backend (Eramba has PHP/Laravel), allowing
  Python-based ingestion scripts that match the rest of our stack
- Has a more complete REST API for batch operations
- Is MIT-licensed (Eramba is AGPL)
- Has first-class support for modern frameworks (NIST CSF 2.0, ISO 27001:2022)

The Eramba-era scripts (`walk_eramba*.py`, `ingest_v1..4.py`,
`phase0*.py`, `inspect_*.py`) are preserved for historical reference but
no longer maintained. The active ingestion path is
`ingest_atlaspay_data.py` (23 KB) and its supporting helpers.

## Stack

| Component | Version |
|---|---|
| CISO Assistant | Community Edition v3.18.3 |
| Caddy | 2.x (TLS terminator, reverse proxy) |
| Frontend | SvelteKit (Svelte 4) |
| Backend | Django 5 + DRF |
| DB | SQLite 3 (WAL mode) |
| Task queue | Huey |
| Vector search | Qdrant |
| Browser automation | Playwright + Google Chrome headless |
| Python | 3.11 |
| Docker Compose | v5.x |
| OS | macOS 26.x |

8 containers total: `caddy`, `frontend`, `backend`, `db` (sqlite file
volume), `huey`, `qdrant`, `mailcatcher`, `flower`.

## Quick start

Prereqs: Docker Desktop, ~4 GB free disk, ports 8443 and 9443 free.

```bash
git clone https://github.com/ijeziermf/atlaspay-grc-sandbox.git
cd atlaspay-grc-sandbox

# Bring up the CISO Assistant stack
docker compose up -d

# Wait ~30s for the backend to migrate + seed
sleep 30
curl -sk -o /dev/null -w '%{http_code}\n' https://localhost:8443/api/health/
# expect: 200
```

Default credentials: `ijeziermf@gmail.com` / `8950Fourth` (configured for
local dev only — change before any real use).

Full walkthrough: see [`docs/00-setup.md`](docs/00-setup.md).

## Repository structure

```
atlaspay-grc-sandbox/
├── README.md                                  ← you are here
├── source-data/
│   └── atlaspay_persona.json                 ← persona definition
├── scripts/
│   ├── ca_api.py                              ← CISO Assistant API client
│   ├── ingest_atlaspay_data.py                ← main ingestion driver (23 KB)
│   ├── ingest_persona.py                     ← persona loader
│   ├── ingest_entities.py                     ← vendor ingestion
│   ├── ingest_policies.py                     ← policy ingestion
│   ├── ingest_risk_scenarios.py               ← risk register ingestion
│   ├── ingest_incidents.py                    ← incident ingestion
│   ├── ingest_assets_bcps.py                  ← asset + BCP ingestion
│   ├── ingest_direct_mysql.py                 ← ORM-bypass ingestion (15 KB)
│   ├── ingest_real_atlaspay.py                ← live REST-based ingestion (18 KB)
│   ├── capture_full_save_cycle.py             ← Playwright save-cycle capture
│   ├── capture_third_parties.py               ← Playwright TPRM capture
│   ├── verify_ca_login.py                     ← auth verification
│   ├── verify_final.py                        ← end-to-end verify
│   ├── verify_live_data.py                    ← live data verify
│   ├── verify_phase_0b.py                     ← phase 0b verify
│   ├── test_crud_api.py                       ← API CRUD probe
│   ├── test_db.php                            ← MySQL probe (historical)
│   ├── walk_eramba.py                          ← [deprecated] Eramba walkthrough
│   ├── walk_eramba_v2.py                       ← [deprecated]
│   ├── walk_eramba_v3.py                       ← [deprecated]
│   ├── ingest_v2.py, v3.py, v4.py              ← [deprecated] Eramba-era
│   ├── phase0a_foundation.py, phase0c_matrix_fix.py  ← [deprecated]
│   ├── inspect_*.py                            ← [deprecated] DOM probes
│   └── ...                                    ← (48 total scripts)
├── screenshots/                               ← PNGs from Playwright runs
├── docs/                                      ← setup notes, lessons learned, ingestion logs
│   ├── 00-setup.md
│   ├── 01-initial-config.md
│   ├── 02-enterprise-gates.md                ← legacy: Eramba CE blockers + workarounds
│   ├── 03-data-ingestion.md
│   ├── 04-real-routes.md
│   ├── ...                                    ← (19 .md files)
│   └── 15-all-traffic.json                   ← captured API traffic from save cycles
└── data/                                      ← anonymized CSV exports (when ready)
```

## Live state verification

```bash
curl -sk -H "Authorization: Token *** https://localhost:8443/api/health/
# {"status":"ok"}

curl -sk -H "Authorization: Token *** \
  "https://localhost:8443/api/folders/?limit=100" | jq '.results[] | .name'
# Expect: AtlasPay, Compliance, Helix Health, Global, ...
```

State counters for the AtlasPay folder (verified 2026-06-24):

| Object | AtlasPay folder |
|---|---|
| Risks | 6 (R-01 through R-06, color-coded levels) |
| Vendors | 7 (Cloud Provider, Payment Gateway, Identity Provider, Application Platform, Monitoring Tools, Finance Systems, Data Warehouse) |
| Contracts | 7 (one MSA per vendor) |
| Policies | 0 in AtlasPay folder (4 in Compliance folder: Access Control, Incident Response, Security Awareness, TPRM) |

## Known limitations

- **Folder filter on REST API is broken** — `?folder=<id>` doesn't filter
  on the nested `{str, id}` object. Filter client-side.
- **Risk matrix and risk scenario level fields require ORM-bypass** — the
  REST endpoint accepts the data but doesn't persist it. Direct Django
  ORM writes via `docker exec backend python` are required.

## Lessons learned

These are documented in detail in
[`docs/PHASE_0_LESSONS_LEARNED.md`](docs/PHASE_0_LESSONS_LEARNED.md). Highlights:

1. Eramba CE v3.30.0 has known vendor bugs that require MySQL bypass
2. Eramba CE blocks 3 critical modules (Risk Calculations, Risk Appetite,
   Identity Governance) to Enterprise tier
3. CISO Assistant v3.18.3 has better ORM access and Python scripting story
4. Auth endpoint: `POST /api/_allauth/app/v1/auth/login` (no trailing slash)
5. Real route names: `/risk-scenarios` not `/risks`, `/perimeters` not `/perimeter`
6. Playwright `install` fails in this env; use `executable_path=/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`

## Related projects

| Repo | Purpose |
|---|---|
| [helix-health-grc-sandbox](https://github.com/ijeziermf/helix-health-grc-sandbox) | HealthTech persona sandbox on the same CISO Assistant instance |
| [meridian-bank-grc-sandbox](https://github.com/ijeziermf/meridian-bank-grc-sandbox) | Community bank persona spec (Phase 0 only) |
| [AtlasPay-Risk-Assessment](https://github.com/ijeziermf/AtlasPay-Risk-Assessment) | Risk register (5x5 matrix, heat map, treatment plan) — historical source for Eramba-era risks |
| [AtlasPay-Risk-Profile-BCP](https://github.com/ijeziermf/AtlasPay-Risk-Profile-BCP) | Business continuity plan |
| [Cyber-Security-Policy-Library](https://github.com/ijeziermf/Cyber-Security-Policy-Library) | Policy templates |
| [Identity-Governance-PIM-RBAC-access-reviews-](https://github.com/ijeziermf/Identity-Governance-PIM-RBAC-access-reviews-) | Account review evidence (CE-gated, but documented) |
| [Scenario-Based-Cyber-Risk-Analyses](https://github.com/ijeziermf/Scenario-Based-Cyber-Risk-Analyses) | Scenario analyses — feeds tabletop exercises |
| [Priviledged-Account-Abuse-Scenario-Analysis](https://github.com/ijeziermf/Priviledged-Account-Abuse-Scenario-Analysis) | Privileged account abuse scenarios |

## Privacy

- No real PII anywhere in this repo
- No real customer data, real vendor names, or real employee names
- AtlasPay is a **simulated FinTech persona** already used in the related public repos
- Screenshots scrub any user-identifying chrome (avatar, email) before commit
- All credentials are local-only

## License

MIT — same as the related Helix and Meridian repos.