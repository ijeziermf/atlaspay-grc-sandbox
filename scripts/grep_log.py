import subprocess
r = subprocess.run(
    ["docker", "compose", "exec", "-T", "eramba", "tail", "-500",
     "/var/www/eramba/app/upgrade/logs/error.log"],
    capture_output=True, text=True, cwd="/Users/ifeanyi/eramba"
)
lines = r.stdout.splitlines()
# Find last AccessControlNodeException
for i, line in enumerate(lines):
    if "AccessControlNodeException" in line and "Risk" in line:
        print("\n".join(lines[max(0,i-3):i+15]))
        print("---")
