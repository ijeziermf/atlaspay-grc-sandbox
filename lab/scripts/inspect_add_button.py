"""Inspect the Add button on /risks — what does it actually do when clicked?"""
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

    # Login
    page.goto(ERAMBA_URL + "/login", wait_until="networkidle", timeout=60000)
    time.sleep(2)
    page.locator("input[name=login]").fill(USER)
    page.locator("input[name=password]").fill(PASS)
    page.locator("button[name=submit]").click()
    page.wait_for_selector("a:has-text('Dashboard')", timeout=30000)
    time.sleep(3)

    # Go to /risks
    page.goto(ERAMBA_URL + "/risks", wait_until="networkidle", timeout=30000)
    time.sleep(3)

    # Snapshot BEFORE
    page.screenshot(path=str(SHOTS / "300-risks-before-add.png"), full_page=True)

    # Find ALL Add-like buttons/links
    add_candidates = page.evaluate("""
        () => {
            const results = [];
            const candidates = document.querySelectorAll('a, button, [class*="add"], [class*="Add"]');
            candidates.forEach(el => {
                const txt = (el.innerText || '').trim().slice(0, 60);
                if (txt.toLowerCase().includes('add') || txt === '+') {
                    results.push({
                        tag: el.tagName.toLowerCase(),
                        text: txt,
                        href: el.getAttribute('href') || '',
                        cls: el.className.toString().slice(0, 100),
                        visible: el.getBoundingClientRect().width > 0,
                        x: Math.round(el.getBoundingClientRect().x),
                        y: Math.round(el.getBoundingClientRect().y),
                        w: Math.round(el.getBoundingClientRect().width),
                        h: Math.round(el.getBoundingClientRect().height)
                    });
                }
            });
            return results;
        }
    """)
    print("Add candidates on /risks:")
    for c in add_candidates[:15]:
        print(f"  <{c['tag']}> text={c['text']!r} visible={c['visible']} pos=({c['x']},{c['y']},{c['w']}x{c['h']})")
        if c['href']:
            print(f"    href={c['href']}")
        if c['cls']:
            print(f"    cls={c['cls'][:80]}")

    # Click each visible Add in turn and screenshot the result
    for c in add_candidates[:5]:
        if not c['visible']:
            continue
        try:
            print(f"\n--- Clicking {c['text']!r} ---")
            loc = page.locator(f"{c['tag']}:has-text('{c['text']}')").first if c['text'] else None
            if loc is None:
                continue
            loc.click(timeout=3000)
            time.sleep(2)
            page.screenshot(path=str(SHOTS / f"301-after-click-{c['text'].replace(' ', '_').replace('/', '-')[:30]}.png"), full_page=True)
            print(f"  URL: {page.url}")
            # Check for modal
            modal = page.evaluate("""
                () => {
                    const m = document.querySelector('[role="dialog"], .modal, [class*="modal"], [class*="Modal"]');
                    if (m) {
                        const inputs = m.querySelectorAll('input, select, textarea');
                        return { found: true, inputs: inputs.length, text: (m.innerText || '').slice(0, 300) };
                    }
                    return { found: false };
                }
            """)
            print(f"  Modal: {modal}")
            # Go back
            page.goto(ERAMBA_URL + "/risks", wait_until="networkidle", timeout=30000)
            time.sleep(2)
        except Exception as e:
            print(f"  ERROR: {e}")
            page.goto(ERAMBA_URL + "/risks", wait_until="networkidle", timeout=30000)
            time.sleep(2)

    browser.close()
