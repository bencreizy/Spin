
import time
import os
import sys
import subprocess

# SOURCE: master_poc_source.py (The code to be typed)
# TARGET: master_poc.py (The file you have open in your editor)
source_path = r'C:\Users\User\master_poc_source.py'

def run_typewriter():
    os.system('cls')
    print("\n[*] Initializing system check...")
    time.sleep(1)
    print("\n[*] Buffer ready. Syncing manifolds in 5 seconds...")
    print("[!] Click the EDITOR WINDOW (master_poc.py) NOW and place cursor at Line 1.")
    
    # Hide the countdown for a cleaner look
    for i in range(5, 0, -1):
        time.sleep(1)

    with open(source_path, 'r') as f:
        lines = f.readlines()

    # We use a PowerShell script block to handle the clipboard and SendKeys
    # This is the most stable way to "type" without character errors.
    print("[*] Initiating secure sync...")
    for line in lines:
        # We escape the line for a PowerShell "Here-String"
        # This prevents any special characters from causing "red errors" in the shell
        clipboard_cmd = f'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Clipboard]::SetText(@\"\n{line.replace("`", "``").replace("$", "`$")}\n\"@)'
        sendkeys_cmd = '$wshell = New-Object -ComObject WScript.Shell; $wshell.SendKeys("^v")'
        
        full_ps_cmd = f'{clipboard_cmd}; {sendkeys_cmd}'
        
        # We run the command hidden so the user doesn't see a popup
        subprocess.run(["powershell", "-WindowStyle", "Hidden", "-Command", full_ps_cmd], capture_output=True)
        
        # Delay for cinematic typing look
        time.sleep(0.4)

    print("\n[+] Sync complete. Finalizing logic verification...")
    time.sleep(1)
    os.system('cls')
    
    # After typing is done, we run the actual python script for the finale
    os.system(f"python C:/Users/User/master_poc.py")

if __name__ == "__main__":
    run_typewriter()
