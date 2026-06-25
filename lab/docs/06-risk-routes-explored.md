# Risk sub-routes explored

All anchors with href=# inside the dropdown:
  'Calculation Method' attrs=data-cy=buttonmenu-item class=relative my-1 flex w-full items-center t href=# data-yjs-request=crud/showForm data-yjs-ta
  'Risk Appetite' attrs=data-cy=buttonmenu-item class=relative my-1 flex w-full items-center t href=# data-yjs-request=crud/showForm data-yjs-ta
  'Classification Types' attrs=data-cy=buttonmenu-item class=relative my-1 flex w-full items-center t href=# data-yjs-request=crud/showForm data-yjs-ta
  'Classifications' attrs=data-cy=buttonmenu-item class=relative my-1 flex w-full items-center t href=# data-yjs-request=crud/showForm data-yjs-ta
  'Residual Risk' attrs=data-cy=buttonmenu-item class=relative my-1 flex w-full items-center t href=# data-yjs-request=crud/showForm data-yjs-ta
  'Reviews' attrs=data-cy=buttonmenu-item class=relative my-1 flex w-full items-center t href=# data-yjs-request=crud/showForm data-yjs-ta
  'Validation Accept' attrs=data-cy=buttonmenu-item class=relative my-1 flex w-full items-center t tabindex=-1 aria-hidden=true data-pc-section=acti
  'Validation Avoid' attrs=data-cy=buttonmenu-item class=relative my-1 flex w-full items-center t tabindex=-1 aria-hidden=true data-pc-section=acti
  'Validation Mitigate' attrs=data-cy=buttonmenu-item class=relative my-1 flex w-full items-center t tabindex=-1 aria-hidden=true data-pc-section=acti
  'Validation Transfer' attrs=data-cy=buttonmenu-item class=relative my-1 flex w-full items-center t tabindex=-1 aria-hidden=true data-pc-section=acti

All <a> tags with real hrefs anywhere on the page now:
  'Asset Risks' -> /risks
  'Third Party Risks' -> /third-party-risks
  'Risk Exceptions' -> /risk-exceptions
  'Asset Risks' -> /risks
  'Reviews' -> /risk-reviews
  'All items
0' -> /risks
  'Threats' -> /risks/threats
  'Vulnerabilities' -> /risks/vulnerabilities
  /risks/classifications -> https://localhost:8443/risks/classifications | 404=False | login_redirect=False | title='DashboardRisk ClassificationsIndex
RiskClassificat'
  /risks/calculation-method -> https://localhost:8443/risks/calculation-method | 404=True | login_redirect=False | title='Not Found'
  /risks/risk-appetite -> https://localhost:8443/risks/risk-appetite | 404=True | login_redirect=False | title='Not Found'
  /risks/classification-types -> https://localhost:8443/risks/classification-types | 404=True | login_redirect=False | title='Not Found'
  /risks/threats -> https://localhost:8443/risks/threats | 404=False | login_redirect=False | title='Asset Risk Threats'
  /risks/vulnerabilities -> https://localhost:8443/risks/vulnerabilities | 404=False | login_redirect=False | title='Asset Risk Vulnerabilities'
  /risks/treatment-options -> https://localhost:8443/risks/treatment-options | 404=True | login_redirect=False | title='Not Found'
  /risks/residual-risk -> https://localhost:8443/risks/residual-risk | 404=True | login_redirect=False | title='Not Found'
  /risks/reviews -> https://localhost:8443/risks/reviews | 404=True | login_redirect=False | title='Not Found'
  /settings/risk-classifications -> https://localhost:8443/settings/risk-classifications | 404=True | login_redirect=False | title='Not Found'
  /settings/risks -> https://localhost:8443/settings/risks | 404=True | login_redirect=False | title='Not Found'
  /risk-classifications -> https://localhost:8443/risk-classifications | 404=False | login_redirect=False | title='DashboardRisk ClassificationsIndex
RiskClassificat'
  /risk-calculations -> https://localhost:8443/risk-calculations | 404=True | login_redirect=False | title='Not Found'

Done.
