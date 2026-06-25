# Phase 1 Skill Build — Tasks for Adeola (after Phase 0 finishes)

**Owner:** Adeola
**Depends on:** Phase 0a (AtlasPay port) verification
**Trigger:** Hermes COO will dispatch via delegate_task when Phase 0 reports done

## 1a. `ciso-assistant-sandbox-bootstrap` skill

**Path:** `~/.hermes/skills/ciso-assistant-sandbox-bootstrap/`

**Purpose:** Spin up a fresh CISO Assistant CE instance via Docker Compose, run auth handshake, seed initial domain tree, return base URL + auth token.

**Inputs:**
- `port` (int, default 8443 for AtlasPay, +1 for each new persona)
- `tenant_name` (string, e.g. "Helix Health")

**Outputs:**
- Running Docker container ID
- Auth token (PAT preferred over session cookie)
- Base URL
- Empty tenant ready for data ingestion

**Components:**
- `SKILL.md` — when to load, prereqs, exact commands
- `scripts/spin_up.sh` — docker compose up with custom port + name
- `scripts/auth.py` — get PAT via /api/_allauth/browser/v1/auth/login (Python urllib, no curl timeouts)
- `scripts/verify_health.py` — hits /api/schema/ + counts /api/folders/
- `references/compose-template.yml` — parameterized CISO Assistant compose file

**Test:** Spin up on port 8444 with tenant name "test-bootstrap", verify auth + folder count = 1, tear down. Total runtime target: under 5 min.

## 1c. `ciso-assistant-screenshot-harness` skill

**Path:** `~/.hermes/skills/ciso-assistant-screenshot-harness/`

**Purpose:** Capture full-page PNG screenshots of CISO Assistant modules with built-in PII scrubbing (auto-crop or skip pages showing user profile/email).

**Inputs:**
- `base_url` (e.g. `https://localhost:8443`)
- `auth_token` (PAT)
- `module_paths` (list, e.g. `["/risk-assessments", "/policies", ...]`)
- `output_dir` (path)
- `filename_prefix` (e.g. "ca-")

**Outputs:**
- N PNG files in `output_dir`, one per module
- Each PNG visually verified to contain records (not empty skeleton)
- PII-safe: never includes profile page, user menu, or session info

**Components:**
- `SKILL.md`
- `scripts/capture.py` — Playwright Python, full-page PNG, auto-wait for SPA hydration
- `scripts/pii_scrub.py` — redaction helper (in case PII leaked into a screenshot)
- `references/module_path_map.json` — CISO Assistant CE v3.18.3 module → URL path
- `scripts/verify_capture.py` — vision check (file size > 10KB, page contains expected text)

**Test against AtlasPay data:** Capture all 6 modules (risks, policies, continuity, vendors, incidents, frameworks), verify each PNG is 50KB+ and contains at least one record name from the ingested data.

## Sequencing

1. Wait for Phase 0a completion (Adeola self)
2. Verify AtlasPay port (count endpoints + screenshot count)
3. Build 1a (sandbox-bootstrap) — needed for Phase 2 (Helix) and Phase 3 (Meridian) tenants
4. Build 1c (screenshot-harness) — needed for Phase 2 and Phase 3 deliverable evidence
5. Return: 2 skill paths, test outputs, any issues
