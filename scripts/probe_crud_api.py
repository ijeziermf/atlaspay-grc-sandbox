"""Find Eramba's CRUD save endpoint structure."""
import re
import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
req = urllib.request.Request(
    'https://localhost:8443/vue_assets/index-D67nL0vi.js',
    headers={'User-Agent': 'Mozilla/5.0'}
)
js = urllib.request.urlopen(req, context=ctx, timeout=20).read().decode('utf-8', errors='ignore')

# Look for the CRUD function
print("=== crud/* patterns ===")
for m in re.finditer(r'crud/[a-z_-]+', js):
    s = max(0, m.start() - 80)
    e = min(len(js), m.end() + 80)
    print(f"  @{m.start()}: ...{js[s:e]}...")
    if len([x for x in re.finditer(r'crud/[a-z_-]+', js)]) > 40:
        break

# Look for how the API is called
print("\n=== t('/api/...') patterns ===")
for m in re.finditer(r'["\']/(api/[^"\']+)', js):
    print(f"  {m.group(1)}")
    if len([x for x in re.finditer(r'["\']/(api/[^"\']+)', js)]) > 20:
        break

# Look for post/put patterns
print("\n=== POST/PUT patterns with paths ===")
for m in re.finditer(r'\.(?:post|put)\s*\(\s*["\']([^"\']+)["\']', js):
    print(f"  {m.group(1)}")
    if len([x for x in re.finditer(r'\.(?:post|put)\s*\(\s*["\']([^"\']+)["\']', js)]) > 30:
        break

# Try the Eramba REST API directly to see what works
print("\n=== Live API probes ===")
api_paths = [
    "/api/risks",
    "/api/security-policies",
    "/api/business-continuity-plans",
    "/api/third-parties",
    "/api/security-incidents",
    "/risks.json",
    "/risks",
]
for path in api_paths:
    try:
        req2 = urllib.request.Request(
            f'https://localhost:8443{path}',
            headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'}
        )
        resp = urllib.request.urlopen(req2, context=ctx, timeout=10)
        print(f"  {path}: {resp.status} {len(resp.read())} bytes")
    except urllib.error.HTTPError as e:
        print(f"  {path}: HTTP {e.code}")
    except Exception as e:
        print(f"  {path}: ERROR {type(e).__name__}: {str(e)[:80]}")
