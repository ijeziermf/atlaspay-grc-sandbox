"""Discover Eramba's REST API endpoints by inspecting the Vue bundle + DOM."""
import re
import urllib.request
import ssl

# Read the Vue bundle to find API endpoint patterns
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(
    'https://localhost:8443/vue_assets/index-D67nL0vi.js',
    headers={'User-Agent': 'Mozilla/5.0'}
)
js = urllib.request.urlopen(req, context=ctx, timeout=20).read().decode('utf-8', errors='ignore')

print(f"Bundle size: {len(js)} bytes")
print()

# Find all API endpoint patterns like '/api/xxx' or '/xxx/save' or 'crud/xxx'
endpoints = set()
for pattern in [
    r'["\'](/[a-z]+/[a-z_-]+(?:/[a-z_-]+)?)["\']',
    r'["\'](/api/[a-z_-]+(?:/[a-z_-]+)?)["\']',
    r'crud/[a-z_-]+',
    r'(?:url|endpoint|path):\s*["\']([^"\']+)["\']',
]:
    for m in re.finditer(pattern, js):
        match = m.group(1) if m.lastindex else m.group(0)
        if any(kw in match for kw in ['crud', 'risk', 'polic', 'vendor', 'incident', 'continuity', 'third-party', 'business-continuity', 'classification']):
            endpoints.add(match.strip('"\''))

print(f"Discovered endpoints ({len(endpoints)}):")
for ep in sorted(endpoints)[:60]:
    print(f"  {ep}")

# Also look for axios/fetch patterns
print("\nFetch/axios patterns:")
for m in re.finditer(r'(?:axios|fetch|\$http|\$ajax)\s*\.\s*(?:post|put|get|delete)\s*\(\s*["\']([^"\']+)', js):
    print(f"  {m.group(1)}")
    if len([x for x in re.finditer(r'(?:axios|fetch|\$http|\$ajax)\s*\.\s*(?:post|put|get|delete)\s*\(', js)]) > 30:
        break
