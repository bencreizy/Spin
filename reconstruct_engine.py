
import time
import os
import sys

source_path = r'C:\Users\User\master_poc_source.py'
target_path = r'C:\Users\User\master_poc.py'

# 1. Clear terminal and initialization
os.system('cls')
print("\n[!] SOURCE MANIFOLD DETECTED. INITIATING EDITOR RECONSTRUCTION...\n")
time.sleep(1)

# 2. Clear target file
with open(target_path, 'w') as f:
    f.write("")

# 3. Read source and type line-by-line
with open(source_path, 'r') as f:
    lines = f.readlines()

for line in lines:
    with open(target_path, 'a') as f:
        f.write(line)
        # Type the actual line content into the terminal (simultaneously)
        sys.stdout.write(line)
        sys.stdout.flush()
    time.sleep(0.3) # Wait for editor refresh + cinematic feel

# 4. Final Handoff to Python logic
print("\n\n[+] RECONSTRUCTION COMPLETE. DEPLOYING EXPLOIT FROM TARGET FILE...")
time.sleep(2)
os.system(f"python {target_path}")
