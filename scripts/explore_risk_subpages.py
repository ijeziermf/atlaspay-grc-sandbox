"""Click through all Risk Settings sub-routes found in dropdown."""
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path.home() / "Documents" / "IfeSec" / "Projects" / "atlaspay-grc-sandbox"
SHOTS = ROOT / "screenshots"
DOCS = ROOT / "docs"
OUT = DOCS / "06-risk-routes-explored.md"
OUT.write_text("# Risk sub-routes explored\n\n")
def log(msg):
    with OUT.open("a") as f:
        f.write(f"{msg}\n")
    print(msg)

ERAMBA_URL = "https://localhost:8443"
USER, PASS = "admin", "8950Fourth"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--ignore-certificate-errors", "--no-sandbox"])
    ctx = browser.new_context(ignore_https_errors=True, viewport={"width": 1440, "height": 900})
    page = ctx.new_page()

    # Login
    page.goto(ERAMBA_URL + "/login", wait_until="networkidle", timeout=60000)
    time.sleep(2)
    page.locator("input[name=login]").fill(USER)
    page.locator("input[name=password]").fill(PASS)
    page.locator("button[name=submit]").click()
    page.wait_for_selector("a:has-text('Dashboard')", timeout=30000)
    time.sleep(3)

    # Open the Risks Settings dropdown to find real URLs
    page.goto(ERAMBA_URL + "/risks", wait_until="networkidle", timeout=30000)
    time.sleep(3)
    settings_btn = page.locator("button[aria-label='Settings']").first
    settings_btn.click()
    time.sleep(2)

    # Find the inner links in the dropdown that might be anchor targets
    log("All anchors with href=# inside the dropdown:")
    anchors = page.evaluate("""
        () => Array.from(document.querySelectorAll('a')).filter(a => a.getAttribute('href') === '#').map(a => {
            const parent = a.closest('div, li, [role="menuitem"]');
            return {
                text: (a.innerText || '').trim(),
                parentText: parent ? (parent.innerText || '').slice(0, 200) : '',
                attrs: Array.from(a.attributes).map(at => `${at.name}=${at.value.slice(0,40)}`).join(' ')
            };
        })
    """)
    for a in anchors[:30]:
        log(f"  '{a['text']}' attrs={a['attrs'][:120]}")

    # Get all <a> tags with non-# hrefs inside any visible menu/popover
    log("\nAll <a> tags with real hrefs anywhere on the page now:")
    links = page.evaluate("""
        () => Array.from(document.querySelectorAll('a[href]:not([href="#"])')).map(a => ({
            text: (a.innerText || '').trim().slice(0, 60),
            href: a.getAttribute('href'),
            visible: a.getBoundingClientRect().width > 0
        })).filter(l => l.visible && l.text.length > 0)
    """)
    for l in links:
        if any(kw in l['href'].lower() for kw in ['risk', 'classification', 'appetite', 'calculation', 'treatment']):
            log(f"  '{l['text']}' -> {l['href']}")

    # Try visiting candidate URLs directly
    candidates = [
        "/risks/classifications",
        "/risks/calculation-method",
        "/risks/risk-appetite",
        "/risks/classification-types",
        "/risks/threats",
        "/risks/vulnerabilities",
        "/risks/treatment-options",
        "/risks/residual-risk",
        "/risks/reviews",
        "/settings/risk-classifications",
        "/settings/risks",
        "/risk-classifications",
        "/risk-calculations",
    ]
    for url in candidates:
        page.goto(ERAMBA_URL + url, wait_until="domcontentloaded", timeout=15000)
        time.sleep(2)
        # Check what we got
        is_404 = "Not Found" in page.inner_text("body")
        is_login = "/login" in page.url
        title = page.evaluate("() => document.querySelector('h1, h2, .page-title')?.innerText || document.title")
        log(f"  {url} -> {page.url} | 404={is_404} | login_redirect={is_login} | title='{title[:50]}'")

    log("\nDone.")
    browser.close()
