"""Capture the EXACT API call Eramba makes when adding a classification.
Fill the form, click Save, capture all XHR/fetch requests and responses."""
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path.home() / "Documents" / "IfeSec" / "Projects" / "atlaspay-grc-sandbox"
SHOTS = ROOT / "screenshots"
ERAMBA_URL = "https://localhost:8443"
USER, PASS = "admin", "8950Fourth"

captured = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--ignore-certificate-errors", "--no-sandbox"])
    ctx = browser.new_context(ignore_https_errors=True, viewport={"width": 1440, "height": 900})
    page = ctx.new_page()

    page.on("request", lambda req: captured.append({
        "phase": "request", "method": req.method, "url": req.url,
        "headers": dict(req.headers),
        "post_data": (req.post_data[:2000] if req.post_data else None),
    }) if ('/laravel/api/' in req.url or 'crud=' in req.url) else None)
    page.on("response", lambda resp: captured.append({
        "phase": "response", "status": resp.status, "url": resp.url,
        "method": resp.request.method,
        "body": (resp.body()[:2000].decode('utf-8', errors='ignore') if resp.body() else None),
    }) if '/laravel/api/' in resp.url else None)

    # Login
    page.goto(ERAMBA_URL + "/login", wait_until="networkidle", timeout=60000)
    time.sleep(2)
    page.locator("input[name=login]").fill(USER)
    page.locator("input[name=password]").fill(PASS)
    page.locator("button[name=submit]").click()
    page.wait_for_selector("a:has-text('Dashboard')", timeout=30000)
    time.sleep(3)

    # /risks/classifications
    page.goto(ERAMBA_URL + "/risks/classifications", wait_until="networkidle", timeout=30000)
    time.sleep(3)

    # Open Actions -> Add
    page.locator("a.dropdown-toggle:has-text('Actions')").first.click()
    time.sleep(1)
    page.locator(".dropdown-menu a:has-text('Add')").first.click()
    page.wait_for_load_state("networkidle", timeout=15000)
    time.sleep(3)
    page.screenshot(path=str(SHOTS / "800-class-add-form.png"), full_page=True)

    # Capture form structure
    inputs = page.evaluate("""
        () => {
            // Get the form that's currently visible (not the list)
            const modals = document.querySelectorAll('.modal, [role="dialog"]');
            const visible = Array.from(modals).filter(m => m.getBoundingClientRect().width > 0);
            const target = visible[0] || document;
            return Array.from(target.querySelectorAll('input, select, textarea')).filter(el => el.getBoundingClientRect().width > 0).map(el => ({
                tag: el.tagName.toLowerCase(),
                type: el.type || '',
                name: el.name || '',
                id: el.id || '',
                placeholder: el.placeholder || '',
                value: el.value || '',
                options: el.tagName === 'SELECT' ? Array.from(el.options).map(o => o.value + '|' + o.text) : null
            }));
        }
    """)
    print("Form inputs visible:")
    for i in inputs:
        print(f"  <{i['tag']}> name={i['name']} id={i['id']} type={i['type']}")
        if i['options']:
            print(f"    options: {i['options']}")

    # Find Save button
    save_buttons = page.evaluate("""
        () => Array.from(document.querySelectorAll('button, input[type=submit]')).filter(el => {
            const r = el.getBoundingClientRect();
            return r.width > 0 && (el.innerText || el.value || '').toLowerCase().match(/save|submit|create|add/);
        }).map(el => ({
            tag: el.tagName.toLowerCase(),
            text: (el.innerText || el.value || '').trim(),
            cls: (el.className || '').toString().slice(0, 100),
            inModal: !!el.closest('.modal, [role="dialog"]'),
            x: Math.round(el.getBoundingClientRect().x),
            y: Math.round(el.getBoundingClientRect().y)
        }))
    """)
    print("\nSave candidates:")
    for b in save_buttons:
        print(f"  <{b['tag']}> '{b['text']}' inModal={b['inModal']} pos=({b['x']},{b['y']}) cls={b['cls'][:60]}")

    # Fill the form (use first available text + number input)
    name_inp = page.locator("input[name=name]:visible").first
    if name_inp.count() > 0:
        name_inp.fill("TestClassification_DO_NOT_KEEP")
        print("\nFilled name")
    value_inp = page.locator("input[name=value]:visible").first
    if value_inp.count() > 0:
        value_inp.fill("5")
        print("Filled value=5")

    page.screenshot(path=str(SHOTS / "801-class-form-filled.png"), full_page=True)

    # Find and click Save (try every save candidate)
    print("\nClicking Save...")
    for sel in [
        ".modal button:has-text('Save')",
        "[role='dialog'] button:has-text('Save')",
        "button.btn-primary",
        "button[type=submit]",
        "button:has-text('Save')",
    ]:
        try:
            btn = page.locator(sel).first
            if btn.is_visible(timeout=2000):
                print(f"  Using selector: {sel}")
                btn.click()
                page.wait_for_load_state("networkidle", timeout=15000)
                time.sleep(3)
                break
        except Exception as e:
            print(f"  {sel}: {type(e).__name__}")

    # Print all captured API calls
    print(f"\n=== {len(captured)} captured API calls ===")
    for c in captured:
        if c.get("phase") == "request":
            print(f"REQ {c['method']} {c['url'][:120]}")
            if c.get('post_data'):
                print(f"  body: {c['post_data'][:300]}")
        else:
            print(f"RESP {c['status']} {c['url'][:120]}")
            if c.get('body'):
                print(f"  body: {c['body'][:300]}")

    # Save everything
    out = ROOT / "docs" / "14-captured-save-cycle.json"
    with out.open("w") as f:
        json.dump(captured, f, indent=2, default=str)
    print(f"\nSaved to {out.name}")

    page.screenshot(path=str(SHOTS / "802-after-save.png"), full_page=True)
    browser.close()
