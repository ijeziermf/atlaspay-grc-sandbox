# AtlasPay Sandbox — v3 final ingestion run

[20:32:18] LOGIN
[20:32:26]   logged in

[20:32:26] STEP 1: Enable Risk Calculation Method (Single Matrix - Addition)
[20:32:34]   -> 700-calc-method-modal.png (116 KB)
[20:32:36]   saved Calculation Method

[20:32:37] STEP 2: Configure Risk Appetite
[20:32:44]   Risk Appetite modal has 0 fields:
[20:32:44]   -> 701-risk-appetite-modal.png (104 KB)
[20:33:14]   ERROR: Locator.click: Timeout 30000ms exceeded.
Call log:
  - waiting for locator(".modal button:has-text('Save'), .modal button.btn-primary").first


[20:33:16] STEP 3: Add Risks (R-01 through R-06)
[20:33:20] 
  ADD: risk R-01
[20:33:20]     WARN: no Actions dropdown or Add item button
[20:33:26] 
  ADD: risk R-02
[20:33:26]     WARN: no Actions dropdown or Add item button
[20:33:31] 
  ADD: risk R-03
[20:33:31]     WARN: no Actions dropdown or Add item button
[20:33:37] 
  ADD: risk R-04
[20:33:37]     WARN: no Actions dropdown or Add item button
[20:33:42] 
  ADD: risk R-05
[20:33:42]     WARN: no Actions dropdown or Add item button
[20:33:48] 
  ADD: risk R-06
[20:33:48]     WARN: no Actions dropdown or Add item button

[20:33:49] STEP 4: Add Policies (4)
[20:33:53] 
  ADD: policy Access Control & Privileged Access Policy
[20:33:55]     form has 0 fields
[20:33:55]       Filling policy: Access Control & Privileged Access Policy
[20:33:55]     WARN: no submit button found
[20:34:01] 
  ADD: policy Incident Response Policy
[20:34:03]     form has 0 fields
[20:34:03]       Filling policy: Incident Response Policy
[20:34:03]     WARN: no submit button found
[20:34:09] 
  ADD: policy Security Awareness & Acceptable Use Policy
[20:34:11]     form has 0 fields
[20:34:11]       Filling policy: Security Awareness & Acceptable Use Policy
[20:34:11]     WARN: no submit button found
[20:34:16] 
  ADD: policy Third-Party Risk Management Policy
[20:34:18]     form has 0 fields
[20:34:18]       Filling policy: Third-Party Risk Management Policy
[20:34:18]     WARN: no submit button found

[20:34:20] STEP 5: Add Continuity Plans (4)
[20:34:24] 
  ADD: BCP Payment Processing BCP
[20:34:26]     form has 0 fields
[20:34:26]       Filling continuity plan: Payment Processing BCP
[20:34:26]     WARN: no submit button found
[20:34:32] 
  ADD: BCP Customer Account Access BCP
[20:34:34]     form has 0 fields
[20:34:34]       Filling continuity plan: Customer Account Access BCP
[20:34:34]     WARN: no submit button found
[20:34:39] 
  ADD: BCP Fraud Monitoring BCP
[20:34:41]     form has 0 fields
[20:34:41]       Filling continuity plan: Fraud Monitoring BCP
[20:34:41]     WARN: no submit button found
[20:34:47] 
  ADD: BCP Financial Reporting BCP
[20:34:49]     form has 0 fields
[20:34:49]       Filling continuity plan: Financial Reporting BCP
[20:34:49]     WARN: no submit button found

[20:34:50] STEP 6: Add Vendors (7)
[20:34:54] 
  ADD: vendor Cloud Provider (Sandbox)
[20:34:56]     form has 0 fields
[20:34:56]       Filling vendor: Cloud Provider (Sandbox)
[20:34:56]     WARN: no submit button found
[20:35:02] 
  ADD: vendor Payment Gateway (Sandbox)
[20:35:04]     form has 0 fields
[20:35:04]       Filling vendor: Payment Gateway (Sandbox)
[20:35:04]     WARN: no submit button found
[20:35:09] 
  ADD: vendor Identity Provider (Sandbox)
[20:35:12]     form has 0 fields
[20:35:12]       Filling vendor: Identity Provider (Sandbox)
[20:35:12]     WARN: no submit button found
[20:35:17] 
  ADD: vendor Application Platform (Sandbox)
[20:35:19]     form has 0 fields
[20:35:19]       Filling vendor: Application Platform (Sandbox)
[20:35:19]     WARN: no submit button found
[20:35:24] 
  ADD: vendor Monitoring Tools (Sandbox)
[20:35:27]     form has 0 fields
[20:35:27]       Filling vendor: Monitoring Tools (Sandbox)
[20:35:27]     WARN: no submit button found
[20:35:32] 
  ADD: vendor Finance Systems (Sandbox)
[20:35:34]     form has 0 fields
[20:35:34]       Filling vendor: Finance Systems (Sandbox)
[20:35:34]     WARN: no submit button found
[20:35:39] 
  ADD: vendor Data Warehouse (Sandbox)
[20:35:42]     form has 0 fields
[20:35:42]       Filling vendor: Data Warehouse (Sandbox)
[20:35:42]     WARN: no submit button found

[20:35:43] STEP 7: Add Sample Incident
[20:35:47] 
  ADD: incident
[20:35:49]     form has 0 fields
[20:35:49]       Filling incident: Sample Phishing Incident - Finance Department
[20:35:49]     WARN: no submit button found

[20:35:51] ======================================================================
[20:35:51] INGESTION SUMMARY (v3)
[20:35:51] ======================================================================
[20:35:51]   Risks:        0 / 6  ([])
[20:35:51]   Policies:     0 / 4  ([])
[20:35:51]   Continuity:   0 / 4  ([])
[20:35:51]   Vendors:      0 / 7  ([])
[20:35:51]   Incidents:    0 / 1  ([])
[20:35:51]   Errors:       23
[20:35:51]     - risk appetite: Locator.click: Timeout 30000ms exceeded.
Call log:
  - waiting for locator(".modal button:has-text('Save'), .modal button.btn-primary").first

[20:35:51]     - risk R-01
[20:35:51]     - risk R-02
[20:35:51]     - risk R-03
[20:35:51]     - risk R-04
[20:35:51]     - risk R-05
[20:35:51]     - risk R-06
[20:35:51]     - policy Access Control & Privileged Access Policy
[20:35:51]     - policy Incident Response Policy
[20:35:51]     - policy Security Awareness & Acceptable Use Policy
[20:35:51]     - policy Third-Party Risk Management Policy
[20:35:51]     - BCP Payment Processing BCP
[20:35:51]     - BCP Customer Account Access BCP
[20:35:51]     - BCP Fraud Monitoring BCP
[20:35:51]     - BCP Financial Reporting BCP
[20:35:51]     - vendor Cloud Provider (Sandbox)
[20:35:51]     - vendor Payment Gateway (Sandbox)
[20:35:51]     - vendor Identity Provider (Sandbox)
[20:35:51]     - vendor Application Platform (Sandbox)
[20:35:51]     - vendor Monitoring Tools (Sandbox)
[20:35:51]     - vendor Finance Systems (Sandbox)
[20:35:51]     - vendor Data Warehouse (Sandbox)
[20:35:51]     - incident
