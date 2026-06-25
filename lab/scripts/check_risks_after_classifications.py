"""After Classifications were added, check if /risks now has an Add button."""
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path.home() / "Documents" / "IfeSec" / "Projects" / "atlaspay-grc-sandbox"
SHOTS = ROOT / "screenshots"
ERAMBA_URL = "https://localhost:8443"
USER, PASS = "admin", "8950Fourth"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--ignore-certificate-errors", "--no-sandbox"])
    ctx = browser.new_context(ignore_https_errors=True, viewport={"width": 1440, "height": 900})
    page = ctx.new_page()

    page.goto(ERAMBA_URL + "/login", wait_until="networkidle", timeout=60000)
    time.sleep(2)
    page.locator("input[name=login]").fill(USER)
    page.locator("input[name=password]").fill(PASS)
    page.locator("button[name=submit]").click()
    page.wait_for_selector("a:has-text('Dashboard')", timeout=30000)
    time.sleep(3)

    # Go to /risks — should now have Add since Classifications exist
    page.goto(ERAMBA_URL + "/risks", wait_until="networkidle", timeout=30000)
    time.sleep(3)
    page.screenshot(path=str(SHOTS / "500-risks-after-classifications.png"), full_page=True)

    # Find all interactive elements with text
    print("=== ALL visible buttons + links on /risks NOW ===")
    items = page.evaluate("""
        () => Array.from(document.querySelectorAll('button, a')).filter(el => el.getBoundingClientRect().width > 0).map(el => ({
            tag: el.tagName.toLowerCase(),
            text: (el.innerText || el.value || '').trim().slice(0, 60),
            href: el.getAttribute('href') || '',
            cls: (el.className || '').toString().slice(0, 80)
        })).filter(el => el.text.length > 0)
    """)
    print(f"Total visible: {len(items)}")
    for i in items[:50]:
        if any(kw in i['text'].lower() for kw in ['add', 'new', 'create', 'risk', 'action', 'classification', 'appetite', 'calculation']):
            print(f"  <{i['tag']}> '{i['text']}' cls={i['cls'][:60]}")

    # Now check /security-policies for its Add pattern
    print("\n\n=== /security-policies ===")
    page.goto(ERAMBA_URL + "/security-policies", wait_until="networkidle", timeout=30000)
    time.sleep(3)
    page.screenshot(path=str(SHOTS / "501-policies-now.png"), full_page=True)
    items2 = page.evaluate("""
        () => Array.from(document.querySelectorAll('button, a')).filter(el => el.getBoundingClientRect().width > 0).map(el => ({
            tag: el.tagName.toLowerCase(),
            text: (el.innerText || el.value || '').trim().slice(0, 60),
            href: el.getAttribute('href') || '',
            cls: (el.className || '').toString().slice(0, 80)
        })).filter(el => el.text.length > 0)
    """)
    for i in items2[:50]:
        if any(kw in i['text'].lower() for kw in ['add', 'new', 'create', 'action']):
            print(f"  <{i['tag']}> '{i['text']}' cls={i['cls'][:60]}")

    # /third-parties
    print("\n\n=== /third-parties ===")
    page.goto(ERAMBA_URL + "/third-parties", wait_until="networkidle", timeout=30000)
    time.sleep(3)
    page.screenshot(path=str(SHOTS / "502-third-parties-now.png"), full_page=True)
    items3 = page.evaluate("""
        () => Array.from(document.querySelectorAll('button, a')).filter(el => el.getBoundingClientRect().width > 0).map(el => ({
            tag: el.tagName.toLowerCase(),
            text: (el.innerText || el.value || '').trim().slice(0, 60),
            href: el.getAttribute('href') || '',
            cls: (el.className || '').toString().slice(0, 80)
        })).filter(el => el.text.length > 0)
    """)
    for i in items3[:50]:
        if any(kw in i['text'].lower() for kw in ['add', 'new', 'create', 'action']):
            print(f"  <{i['tag']}> '{i['text']}' cls={i['cls'][:60]}")

    browser.close()
