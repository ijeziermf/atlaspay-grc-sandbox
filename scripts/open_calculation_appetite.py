"""Click Calculation Method + Risk Appetite + Classification Types to see forms."""
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path.home() / "Documents" / "IfeSec" / "Projects" / "atlaspay-grc-sandbox"
SHOTS = ROOT / "screenshots"
ERAMBA_URL = "https://localhost:8443"
USER, PASS = "admin", "8950Fourth"

def dump_inputs(page, label):
    """Dump form inputs to stdout."""
    inputs = page.evaluate("""
        () => Array.from(document.querySelectorAll('input, select, textarea')).filter(el => el.getBoundingClientRect().width > 0).map(el => ({
            tag: el.tagName.toLowerCase(),
            type: el.type || '',
            name: el.name || '',
            id: el.id || '',
            placeholder: el.placeholder || '',
            value: el.value || '',
            options: el.tagName === 'SELECT' ? Array.from(el.options).map(o => o.value + ':' + o.text) : null
        }))
    """)
    print(f"  {label}: {len(inputs)} inputs")
    for i in inputs:
        if i['tag'] in ('select',) and i['options']:
            print(f"    <{i['tag']}> name={i['name']} id={i['id']} options={i['options']}")
        else:
            print(f"    <{i['tag']}> type={i['type']} name={i['name']} id={i['id']} placeholder={i['placeholder']} value='{i['value'][:40]}'")

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

    page.goto(ERAMBA_URL + "/risks", wait_until="networkidle", timeout=30000)
    time.sleep(3)

    # Open Settings dropdown
    page.locator("button[aria-label='Settings']").first.click()
    time.sleep(2)

    # Click each setting, dump its form, close
    for setting in ["Calculation Method", "Risk Appetite", "Classification Types", "Treatment Options", "Residual Risk"]:
        try:
            print(f"\n=== {setting} ===")
            # The dropdown may have closed; re-open if needed
            link = page.locator(f"a:has-text('{setting}')").first
            if not link.is_visible(timeout=2000):
                # Re-open dropdown
                page.locator("button[aria-label='Settings']").first.click()
                time.sleep(1)
                link = page.locator(f"a:has-text('{setting}')").first
            link.click()
            page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(2)
            shot_name = f"620-{setting.lower().replace(' ', '-')}"
            page.screenshot(path=str(SHOTS / f"{shot_name}.png"), full_page=True)
            dump_inputs(page, setting)
            # Close the modal
            page.keyboard.press("Escape")
            time.sleep(1)
        except Exception as e:
            print(f"  ERROR: {e}")

    browser.close()
