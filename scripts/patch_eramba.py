"""
Patch RisksTable.php to add the missing findClassifications() method.
This is a workaround for Eramba CE v3.30.0 bug where findForm() calls
->find('classifications') but the finder doesn't exist.
"""
import subprocess

# The stub method to insert
STUB = '''    /**
     * Stub: classifications finder (workaround for Eramba CE v3.30.0 bug).
     * Returns the query as-is; classifications are loaded separately by the API.
     *
     * @param \\Cake\\ORM\\Query $query
     * @return \\Cake\\ORM\\Query
     */
    public function findClassifications(Query $query)
    {
        return $query;
    }

'''

# Read the current file
r = subprocess.run(
    ["docker", "compose", "exec", "-T", "eramba", "cat",
     "/var/www/eramba/app/upgrade/src/Model/Table/RisksTable.php"],
    capture_output=True, text=True, cwd="/Users/ifeanyi/eramba"
)
content = r.stdout
print(f"File length: {len(content)} bytes")

# Find the findForm method and insert the stub before it
needle = "    public function findForm(Query $query)"
if needle not in content:
    print("ERROR: could not find findForm method")
    exit(1)

# Insert the stub before findForm
patched = content.replace(needle, STUB + needle, 1)
print(f"Patched length: {len(patched)} bytes (+{len(patched) - len(content)})")

# Write the patched file back via docker exec
# Use a temp file approach
patched_escaped = patched.replace("'", "'\\''")

# Write to a temp file inside the container via cat << EOF
result = subprocess.run(
    ["docker", "compose", "exec", "-T", "eramba", "bash", "-c",
     f"cat > /tmp/RisksTable.php << 'PHP_EOF'\n{patched}\nPHP_EOF\n"
     "echo 'Wrote /tmp/RisksTable.php' && wc -l /tmp/RisksTable.php"],
    capture_output=True, text=True, cwd="/Users/ifeanyi/eramba"
)
print("Container write:", result.stdout)
print("Container write err:", result.stderr)

# Copy it over the original
result2 = subprocess.run(
    ["docker", "compose", "exec", "-T", "eramba", "bash", "-c",
     "cp /tmp/RisksTable.php /var/www/eramba/app/upgrade/src/Model/Table/RisksTable.php && "
     "chown www-data:www-data /var/www/eramba/app/upgrade/src/Model/Table/RisksTable.php && "
     "echo 'Copied successfully' && wc -l /var/www/eramba/app/upgrade/src/Model/Table/RisksTable.php"],
    capture_output=True, text=True, cwd="/Users/ifeanyi/eramba"
)
print("Copy:", result2.stdout)
print("Copy err:", result2.stderr)

# Verify the patch is in place
verify = subprocess.run(
    ["docker", "compose", "exec", "-T", "eramba", "bash", "-c",
     "grep -n 'findClassifications' /var/www/eramba/app/upgrade/src/Model/Table/RisksTable.php"],
    capture_output=True, text=True, cwd="/Users/ifeanyi/eramba"
)
print("\nVerification (should show 2 lines: def + call):")
print(verify.stdout)
