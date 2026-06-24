# AtlasPay Sandbox — v4 ingestion (save-btn + classification type first)

[20:42:21] LOGIN
[20:42:30]   logged in

[20:42:30] STEP 0: Enable Risk Calculation Method
[20:42:40]   saved Calculation Method

[20:42:41] STEP 1: Configure Risk Appetite

[20:42:50] STEP 2: Add Classification Types (Impact, Likelihood)
[20:42:54] 
  Adding classification type: Impact
[20:42:58]     filled name=Impact
[20:42:58]   -> 900-classtype-Impact-form.png
[20:43:00]     added
[20:43:04] 
  Adding classification type: Likelihood
[20:43:07]     filled name=Likelihood
[20:43:07]   -> 900-classtype-Likelihood-form.png
[20:43:09]     added
[20:43:13]   -> 901-classtypes-after.png

[20:43:13] STEP 3: Add Classifications (Critical/High/Medium/Low/Very Low)
[20:43:17] 
  Adding classification: Critical (value=20)
[20:43:20]     type options: [('', '')]
[20:43:20]   -> 910-classification-Critical-form.png
[20:43:22]     added
[20:43:26] 
  Adding classification: High (value=12)
[20:43:29]     type options: [('', '')]
[20:43:29]   -> 910-classification-High-form.png
[20:43:31]     added
[20:43:35] 
  Adding classification: Medium (value=8)
[20:43:38]     type options: [('', '')]
[20:43:38]   -> 910-classification-Medium-form.png
[20:43:40]     added
[20:43:45] 
  Adding classification: Low (value=4)
[20:43:48]     type options: [('', '')]
[20:43:48]   -> 910-classification-Low-form.png
[20:43:50]     added
[20:43:54] 
  Adding classification: Very Low (value=2)
[20:43:57]     type options: [('', '')]
[20:43:57]   -> 910-classification-Very Low-form.png
[20:43:59]     added
[20:44:03]   -> 911-classifications-final.png

[20:44:03] STEP 4: Add Risks (R-01 through R-06)
[20:44:03] 
  Adding risk R-01: Phishing Attacks
[20:44:07]     WARN: no Add button
[20:44:07] 
  Adding risk R-02: Access Control Weakness
[20:44:11]     WARN: no Add button
[20:44:11] 
  Adding risk R-03: Logging and Monitoring Gaps
[20:44:15]     WARN: no Add button
[20:44:15] 
  Adding risk R-04: Incident Response Planning and Testing
[20:44:19]     WARN: no Add button
[20:44:19] 
  Adding risk R-05: Third-Party and Vendor Risk Management
[20:44:23]     WARN: no Add button
[20:44:23] 
  Adding risk R-06: Security Awareness and Training
[20:44:27]     WARN: no Add button
[20:44:27]   -> 921-risks-final.png

[20:44:27] STEP 5: Add Policies (4)
[20:44:27] 
  Adding policy: Access Control & Privileged Access Policy
[20:44:33]   -> 930-policy-form.png
[20:44:35] 
  Adding policy: Incident Response Policy
[20:44:41]   -> 930-policy-form.png
[20:44:42] 
  Adding policy: Security Awareness & Acceptable Use Policy
[20:44:48]   -> 930-policy-form.png
[20:44:50] 
  Adding policy: Third-Party Risk Management Policy
[20:44:56]   -> 930-policy-form.png
[20:44:58]   -> 931-policies-final.png

[20:44:58] STEP 6: Add Continuity Plans (4)
[20:44:58] 
  Adding BCP: Payment Processing BCP
[20:45:04]   -> 940-bcp-form.png
[20:45:05] 
  Adding BCP: Customer Account Access BCP
[20:45:11]   -> 940-bcp-form.png
[20:45:13] 
  Adding BCP: Fraud Monitoring BCP
[20:45:19]   -> 940-bcp-form.png
[20:45:20] 
  Adding BCP: Financial Reporting BCP
[20:45:26]   -> 940-bcp-form.png
[20:45:28]   -> 941-bcp-final.png

[20:45:28] STEP 7: Add Vendors (7)
[20:45:28] 
  Adding vendor: Cloud Provider (Sandbox)
[20:45:34]   -> 950-vendor-form.png
[20:45:36] 
  Adding vendor: Payment Gateway (Sandbox)
[20:45:42]   -> 950-vendor-form.png
[20:45:43] 
  Adding vendor: Identity Provider (Sandbox)
[20:45:49]   -> 950-vendor-form.png
[20:45:51] 
  Adding vendor: Application Platform (Sandbox)
[20:45:57]   -> 950-vendor-form.png
[20:45:58] 
  Adding vendor: Monitoring Tools (Sandbox)
[20:46:05]   -> 950-vendor-form.png
[20:46:06] 
  Adding vendor: Finance Systems (Sandbox)
[20:46:12]   -> 950-vendor-form.png
[20:46:14] 
  Adding vendor: Data Warehouse (Sandbox)
[20:46:20]   -> 950-vendor-form.png
[20:46:21]   -> 951-vendors-final.png

[20:46:21] STEP 8: Add Sample Incident
[20:46:27]   -> 960-incident-form.png
[20:46:29]   -> 961-incidents-final.png

[20:46:29] ======================================================================
[20:46:29] INGESTION SUMMARY (v4)
[20:46:29] ======================================================================
[20:46:29]   Risks:        0 / 6  ([])
[20:46:29]   Policies:     0 / 4  ([])
[20:46:29]   Continuity:   0 / 4  ([])
[20:46:29]   Vendors:      0 / 7  ([])
[20:46:29]   Incidents:    0 / 1  ([])
[20:46:29] 
  Errors (15):
[20:46:29]     - policy Access Control & Privileged Access Policy: save failed
[20:46:29]     - policy Incident Response Policy: save failed
[20:46:29]     - policy Security Awareness & Acceptable Use Policy: save failed
[20:46:29]     - policy Third-Party Risk Management Policy: save failed
[20:46:29]     - BCP Payment Processing BCP: save failed
[20:46:29]     - BCP Customer Account Access BCP: save failed
[20:46:29]     - BCP Fraud Monitoring BCP: save failed
[20:46:29]     - BCP Financial Reporting BCP: save failed
[20:46:29]     - vendor Cloud Provider (Sandbox): save failed
[20:46:29]     - vendor Payment Gateway (Sandbox): save failed
[20:46:29]     - vendor Identity Provider (Sandbox): save failed
[20:46:29]     - vendor Application Platform (Sandbox): save failed
[20:46:29]     - vendor Monitoring Tools (Sandbox): save failed
[20:46:29]     - vendor Finance Systems (Sandbox): save failed
[20:46:29]     - vendor Data Warehouse (Sandbox): save failed
