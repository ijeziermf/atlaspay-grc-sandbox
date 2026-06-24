# Two-Sandbox Portfolio Expansion — Active Execution Plan

**Owner:** Hermes COO (IfeSec)
**Approved:** 2026-06-23 ~10:48 EDT
**Architectural decision:** Architecture A — single CISO Assistant CE v3.18.3 instance at https://localhost:8443, one domain per client/persona (AtlasPay, Helix Health, Meridian Bank). Domain tree IS the isolation boundary. No separate Docker instances per persona.
**Reference doc:** `~/Documents/IfeSec/Projects/ciso-assistant-portfolio-expansion-proposal.md` (183 lines, Architecture A rationale)
**Discord ping:** Phase 0 + Phase 1 complete → post to `#📜｜agent-logs` in HQ IfeSec Discord

---

## Why Architecture A (not separate Docker per persona)

Single CISO Assistant instance, domains = sandbox boundaries. Reasons:
- Lower resource footprint (one MySQL, one Redis, one app container, ~2GB RAM total vs 6GB for 3 instances)
- One login, one PAT rotation, one SMTP config
- Cross-persona analytics built-in (e.g. "show me all critical risks across my 3 client sandboxes")
- Domains in CISO Assistant are explicitly designed as multi-tenant isolation — folder-level perms, scoped perimeters, audit log partitioning
- Matches the actual deployment pattern Ijezie Risk Advisory will use at scale (one tenant for IfeSec's own GRC + one domain per active client engagement)

This is the prior session's recommendation; I align with it.

---

## Domain structure (target end state)

```
https://localhost:8443   ← single CE instance, one login
├── Domain: "AtlasPay" (Sandbox)        ← existing — leave untouched after Phase 0
│   ├── Perimeter: AtlasPay Core Payment System
│   ├── Perimeter: AtlasPay Data Platform
│   ├── Frameworks: SOC 2 TSC, NIST CSF 2.0, ISO 27001:2022 (loaded)
│   ├── 6 risks (R-01..R-06)
│   ├── 4 policies (ACC-01, IR-01, SA-01, TPRM-01)
│   ├── 4 continuity plans
│   ├── 7 vendors
│   └── 1 incident
│
├── Domain: "Helix Health" (Sandbox)    ← NEW — Phase 2
│   ├── Perimeter: BAA-Scope PHI Processing System
│   ├── Perimeter: Helix Provider Portal
│   ├── Perimeter: Helix Internal Infrastructure
│   ├── Frameworks: HIPAA, HITRUST CSF, SOC 2 TSC
│   ├── Healthcare SaaS persona: 200 employees, 30 vendors, 12 PHI processing systems
│   └── Privacy Register (ROPA)
│
└── Domain: "Meridian Bank" (Sandbox)   ← NEW — Phase 3
    ├── Perimeter: Meridian Retail Banking
    ├── Perimeter: Meridian Loan Origination
    ├── Perimeter: Meridian Treasury
    ├── Perimeter: Meridian Digital Channels
    ├── Frameworks: FFIEC CAT, GLBA Safeguards, SOC 2 TSC
    ├── Community bank persona: $2B AUM, 40 vendors
    └── EBIOS RM workshop outputs
```

---

## Active phase plan

### Phase 0 — AtlasPay re-port to CISO Assistant v3.18.3
**Owner:** Adeola (subagent `deleg_7d129e1d`)
**Status:** IN PROGRESS
**Started:** 2026-06-23 ~10:50 EDT

**Tasks:**
1. Verify auth (Python urllib, no curl timeouts)
2. Build domain tree: Root → AtlasPay → (Engineering, Operations, Finance, Compliance)
3. Load frameworks: SOC 2 TSC, NIST CSF 2.0, ISO 27001:2022 (one-shot library load)
4. Create 2 perimeters (AtlasPay-Payments, AtlasPay-Data)
5. Ingest 22 records via MCP/REST: 6 risks, 4 policies, 4 continuity, 7 vendors, 1 incident
6. Verify via API count (NOT "added" log lines)
7. Capture 6 PII-scrubbed screenshots

**Deliverables for Hermes verification:**
- API count JSON for all 9 model endpoints
- 6 PNG files at `~/Documents/IfeSec/Projects/atlaspay-grc-sandbox/screenshots/ca-{01-06}-*.png`
- 10+ scripts in `~/Documents/IfeSec/Projects/atlaspay-grc-sandbox/scripts/`

### Phase 1 — Three reusable skills

| Skill | Owner | Status | Path | Purpose |
|---|---|---|---|---|
| `ciso-assistant-sandbox-bootstrap` | Adeola | Pending | `~/.hermes/skills/ciso-assistant-sandbox-bootstrap/` | Spin up CE instance, auth handshake, seed domain tree |
| `ciso-assistant-portfolio-pdf` | Amara (subagent `deleg_2315775c`) | IN PROGRESS | `~/.hermes/skills/ciso-assistant-portfolio-pdf/` | IfeSec-branded PDF generator (black/gold/crimson) |
| `ciso-assistant-screenshot-harness` | Adeola | Pending | `~/.hermes/skills/ciso-assistant-screenshot-harness/` | Playwright capture + auto PII scrub |

**Gate:** All 3 skills built, tested against Phase 0 AtlasPay data, SKILL.md present, working example output.

### Phase 2 — Helix Health (parallel-ready)
- HIPAA + HITRUST + SOC 2 frameworks
- Persona: Healthcare SaaS, 200 employees, BAA-covered PHI, 30 vendors
- Modules exercised: Privacy Register (ROPA), Validation Flows (multi-approver), audit log forwarding to Datadog
- Published repos: `ijeziermf/Helix-Health-Risk-Assessment`, `ijeziermf/Helix-Health-Compliance-Audit`
- Sandbox repo: `helix-health-grc-sandbox/` (local, push after Phase 4)

### Phase 3 — Meridian Bank (parallel-ready)
- FFIEC CAT + GLBA Safeguards + SOC 2 TSC frameworks
- Persona: Community bank, $2B AUM, 40 vendors
- Modules exercised: EBIOS RM (workshop-driven), Kafka SIEM forwarding, exam-ready sign-off
- Published repos: `ijeziermf/Meridian-Bank-Risk-Profile`, `ijeziermf/Meridian-Bank-TPRM-Framework`
- Sandbox repo: `meridian-bank-grc-sandbox/` (local, push after Phase 4)

### Phase 4 — Cross-portfolio integration
- LinkedIn announcement post (Amara)
- Portfolio site update (`ijeziermf.github.io/portfolio/`)
- Resume tailor pass (add 2 new entries)
- Mission Control dashboard updates (Ugo)
- GitHub repo pushes (all 3 sandbox repos + 4 published repos, total 7 new public repos)

---

## Council assignments

| Phase | Adeola (automation) | Amara (brand) | Obinna (security) | Ugo (orchestrator) | Hermes (COO) |
|---|---|---|---|---|---|
| 0 — AtlasPay port | Lead | — | Framework selection sign-off | — | Verify gates + post Discord |
| 1 — Skills | sandbox-bootstrap, screenshot-harness | portfolio-pdf | HIPAA/HITRUST/FFIEC validation | — | Skill review + integration test |
| 2 — Helix | Ingest scripts + screenshots | PDF narrative + brand voice | HIPAA/HITRUST sign-off | Status updates | GitHub publish gate |
| 3 — Meridian | Ingest scripts + screenshots | PDF narrative | FFIEC methodology sign-off | Status updates | GitHub publish gate |
| 4 — Integration | Portfolio site update | LinkedIn post + brand consistency | — | Mission Control rollup | Final summary + Discord close |

---

## Your review gates

1. **After Phase 0:** Open `https://localhost:8443`, click through the 6 AtlasPay modules, confirm records are visible and no PII leaked. (5 min)
2. **After Phase 2:** Review 2 Helix published PDFs before I push to GitHub. (15 min)
3. **After Phase 3:** Review 2 Meridian published PDFs before I push to GitHub. (15 min)
4. **Phase 4:** Approve LinkedIn post + portfolio site updates before any publish. (10 min)

---

## Discord message format (Phase 0+1 complete)

Posted to `#📜｜agent-logs` (channel ID `1499630253050429581`):

```
✅ Phase 0+1 Complete — AtlasPay ported + 3 skills built

CISO Assistant v3.18.3 (verified via /api/ count):
  • folders: 6 (Root + AtlasPay + 4 depts)
  • perimeters: 2
  • risk-assessments: 6
  • policies: 4
  • business-continuity-plans: 4
  • third-parties: 7
  • incidents: 1
  • frameworks: 3 (SOC 2 TSC, NIST CSF 2.0, ISO 27001:2022)

Screenshots (PII-scrubbed):
  ~/Documents/IfeSec/Projects/atlaspay-grc-sandbox/screenshots/ca-{01-06}-*.png

Skills built:
  • ~/.hermes/skills/ciso-assistant-sandbox-bootstrap/
  • ~/.hermes/skills/ciso-assistant-portfolio-pdf/
  • ~/.hermes/skills/ciso-assistant-screenshot-harness/

Ready to start Phase 2 (Helix Health) + Phase 3 (Meridian Bank) in parallel.
Open https://localhost:8443 to visually verify.
```

---

## Timeline

- **Phase 0:** 2026-06-23 (today) — AtlasPay re-port via Adeola subagent
- **Phase 1:** 2026-06-23 to 2026-06-24 — 3 skills built (Amara in flight now, Adeola after Phase 0)
- **Phase 2:** 2026-06-24 to 2026-06-26 — Helix Health sandbox
- **Phase 3:** 2026-06-26 to 2026-06-28 — Meridian Bank sandbox (can run parallel with Phase 2)
- **Phase 4:** 2026-06-29 — Cross-portfolio integration + 7 GitHub pushes
- **Total:** ~7 calendar days, mostly autonomous on my side
