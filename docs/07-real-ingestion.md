# AtlasPay Sandbox — Real data ingestion run

[20:19:40] ======================================================================
[20:19:40] AtlasPay Sandbox — REAL data ingestion
[20:19:40] ======================================================================
[20:19:40] Risks: 6, Policies: 4, 
[20:19:40] Continuity: 4, Vendors: 7, 
[20:19:40] Incidents: 1

[20:19:41] LOGIN
[20:19:50]   logged in, URL: https://localhost:8443/dashboard

[20:19:50] STEP 1: Add Risk Classifications (5 levels: Critical/High/Medium/Low/Very Low)
[20:19:54]   -> 200-classifications-empty.png (79 KB)
[20:19:54]   Adding classification: Critical (value=20)
[20:19:59]     ERROR: Locator.click: Timeout 5000ms exceeded.
Call log:
  - waiting for get_by_role("link", name="Add").first

[20:19:59]   Adding classification: High (value=12)
[20:20:04]     ERROR: Locator.click: Timeout 5000ms exceeded.
Call log:
  - waiting for get_by_role("link", name="Add").first

[20:20:04]   Adding classification: Medium (value=8)
[20:20:09]     ERROR: Locator.click: Timeout 5000ms exceeded.
Call log:
  - waiting for get_by_role("link", name="Add").first

[20:20:09]   Adding classification: Low (value=4)
[20:20:14]     ERROR: Locator.click: Timeout 5000ms exceeded.
Call log:
  - waiting for get_by_role("link", name="Add").first

[20:20:14]   Adding classification: Very Low (value=2)
[20:20:19]     ERROR: Locator.click: Timeout 5000ms exceeded.
Call log:
  - waiting for get_by_role("link", name="Add").first

[20:20:19]   -> 201-classifications-after.png (79 KB)

[20:20:19] STEP 2: Add Risks (R-01 through R-06)
[20:20:23]   Adding risk R-01: Phishing Attacks
[20:20:28]     ERROR: Locator.click: Timeout 5000ms exceeded.
Call log:
  - waiting for get_by_role("button", name="Add").first

[20:20:28]   Adding risk R-02: Access Control Weakness
[20:20:33]     ERROR: Locator.click: Timeout 5000ms exceeded.
Call log:
  - waiting for get_by_role("button", name="Add").first

[20:20:33]   Adding risk R-03: Logging and Monitoring Gaps
[20:20:38]     ERROR: Locator.click: Timeout 5000ms exceeded.
Call log:
  - waiting for get_by_role("button", name="Add").first

[20:20:38]   Adding risk R-04: Incident Response Planning and Testing
[20:20:43]     ERROR: Locator.click: Timeout 5000ms exceeded.
Call log:
  - waiting for get_by_role("button", name="Add").first

[20:20:43]   Adding risk R-05: Third-Party and Vendor Risk Management
[20:20:48]     ERROR: Locator.click: Timeout 5000ms exceeded.
Call log:
  - waiting for get_by_role("button", name="Add").first

[20:20:48]   Adding risk R-06: Security Awareness and Training
[20:20:53]     ERROR: Locator.click: Timeout 5000ms exceeded.
Call log:
  - waiting for get_by_role("button", name="Add").first

[20:20:53]   -> 210-risks-after.png (103 KB)

[20:20:53] STEP 3: Add Policies (4)
