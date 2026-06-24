"""Inspect /risks/classifications — what Add form does it use?"""
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

    page.goto(ERAMBA_URL + "/risks/classifications", wait_until="networkidle", timeout=30000)
    time.sleep(3)
    page.screenshot(path=str(SHOTS / "310-classifications.png"), full_page=True)

    # Find ALL buttons + their text
    print("=== ALL BUTTONS ON /risks/classifications ===")
    btns = page.evaluate("""
        () => Array.from(document.querySelectorAll('button, a')).map(el => ({
            tag: el.tagName.toLowerCase(),
            text: (el.innerText || el.value || '').trim().slice(0, 60),
            href: el.getAttribute('href') || '',
            visible: el.getBoundingClientRect().width > 0,
            cls: (el.className || '').toString().slice(0, 80)
        })).filter(el => el.visible && el.text.length > 0 && el.text.length < 60)
    """)
    for b in btns[:30]:
        print(f"  <{b['tag']}> '{b['text']}' visible={b['visible']} cls={b['cls'][:60]}")
        if b['href'] and b['href'] != '#':
            print(f"    href={b['href']}")

    # Look for an inline form already on the page
    print("\n=== ALL INPUTS ON /risks/classifications ===")
    inputs = page.evaluate("""
        () => Array.from(document.querySelectorAll('input, select, textarea')).map(el => ({
            tag: el.tagName.toLowerCase(),
            type: el.type || '',
            name: el.name || '',
            id: el.id || '',
            placeholder: el.placeholder || '',
            visible: el.getBoundingClientRect().width > 0,
            value: el.value || ''
        }))
    """)
    for i in inputs:
        print(f"  <{i['tag']}> type={i['type']} name={i['name']} id={i['id']} visible={i['visible']}")

    browser.close()
