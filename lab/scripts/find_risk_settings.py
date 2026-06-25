"""Click into Risk Management to find real Risk Settings sub-routes."""
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path.home() / "Documents" / "IfeSec" / "Projects" / "atlaspay-grc-sandbox"
SHOTS = ROOT / "screenshots"
DOCS = ROOT / "docs"
OUT = DOCS / "05-risk-settings-discovery.md"
OUT.write_text("# Risk Settings route discovery\n\n")
def log(msg):
    with OUT.open("a") as f:
        f.write(f"[{time.strftime('%H:%M:%S')}] {msg}\n")
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

    # Click Risk Management
    log("Clicking 'Risk Management' in sidebar...")
    page.locator("a:has-text('Risk Management')").first.click(timeout=5000)
    time.sleep(2)
    page.screenshot(path=str(SHOTS / "110-risk-management-expanded.png"), full_page=True)
    log(f"  URL: {page.url}")

    # Enumerate all visible links after expansion
    links = page.evaluate("""
        () => Array.from(document.querySelectorAll('a')).map(a => ({
            text: (a.innerText || '').trim().slice(0, 60),
            href: a.getAttribute('href') || '',
            visible: a.getBoundingClientRect().width > 0
        })).filter(l => l.href && l.visible && l.text.length > 0)
    """)
    log("\nLinks visible after clicking Risk Management:")
    for l in links:
        log(f"  '{l['text']}' -> {l['href']}")

    # Try clicking Asset Risks to see the page
    log("\n\nClicking 'Asset Risks' submenu...")
    try:
        page.locator("a:has-text('Asset Risks')").first.click(timeout=5000)
        time.sleep(2)
        page.screenshot(path=str(SHOTS / "111-asset-risks-after-click.png"), full_page=True)
        log(f"  URL: {page.url}")

        # Look for "Settings" or "Configure" buttons on the risks page
        links2 = page.evaluate("""
            () => Array.from(document.querySelectorAll('a, button')).map(el => ({
                tag: el.tagName.toLowerCase(),
                text: (el.innerText || '').trim().slice(0, 60),
                href: el.getAttribute('href') || '',
                visible: el.getBoundingClientRect().width > 0
            })).filter(l => l.visible && l.text.length > 0)
        """)
        log("\nButtons/links visible on Asset Risks page:")
        for l in links2:
            if 'risk' in l['text'].lower() or 'setting' in l['text'].lower() or 'config' in l['text'].lower():
                log(f"  <{l['tag']}> '{l['text']}' -> {l['href']}")
    except Exception as e:
        log(f"  Asset Risks click failed: {e}")

    # Look for settings cog/gear icon in the risks page
    log("\nLooking for the settings cog icon (often near page title)...")
    cogs = page.evaluate("""
        () => Array.from(document.querySelectorAll('a, button, [class*="cog"], [class*="setting"], [class*="gear"]')).map(el => ({
            tag: el.tagName.toLowerCase(),
            cls: el.className || '',
            text: (el.innerText || '').trim().slice(0, 60),
            title: el.title || '',
            ariaLabel: el.getAttribute('aria-label') || '',
            href: el.getAttribute('href') || ''
        })).filter(el => el.cls.toLowerCase().includes('setting') || el.cls.toLowerCase().includes('cog') ||
                          el.text.toLowerCase().includes('setting') || el.title.toLowerCase().includes('setting') ||
                          el.title.toLowerCase().includes('risk') || el.ariaLabel.toLowerCase().includes('setting'))
    """)
    for c in cogs[:10]:
        log(f"  {c}")

    log("\nDone.")
    browser.close()
