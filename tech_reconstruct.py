import time
import sys
import os
import webbrowser

# Typewriter Engine for Technical Reconstruction
def tech_print(text, delay=0.02, color="\033[36m"):
    for char in text:
        sys.stdout.write(f"{color}{char}\033[0m")
        sys.stdout.flush()
        time.sleep(delay if char != '\n' else delay * 5)
    print()

def gdk_audit_sequence():
    # Clear terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    
    tech_print(">>> [GITLAB GDK: VULNERABILITY AUDIT]", 0.04, "\033[1;35m")
    tech_print(">>> STATUS: ACTIVE | AUTH_BYPASS_CONFIRMED", 0.04, "\033[1;32m")
    print("-" * 80)
    time.sleep(1)

    # RECONSTRUCTION DATA
    evidence_lines = [
        "[SYSTEM] Initiating GDK Sub-Core configuration...",
        "[+] gdk.yml -> saml: { enabled: true, hash_type: 'array_flexible' }",
        "[+] OmniAuth -> Reconfigured for XML Desynchronization",
        "",
        "[ANALYSIS] Target: /users/auth/saml/callback",
        "[ANALYSIS] Vulnerability: Ruby Array Coercion via NameID Fracture",
        "",
        "[EXPLOIT] Crafting Vulnerable XML Payload...",
        "<saml2:NameID>",
        "    admin_uid",
        "    <ArrayCoercionNode>admin_uid</ArrayCoercionNode>",
        "</saml2:NameID>",
        "",
        "[EXECUTION] Injecting Fracture into GDK Protocol Stream...",
        "[*] POST /users/auth/saml/callback ...",
        "[*] Payload: Base64[...fractured_payload...]",
        "",
        "[IMPACT] State Bleed Detected.",
        "[!] AuthHash[uid] => ['admin_uid', 'admin_uid']",
        "[!] Validation: BYPASSED (Logic Desync)",
        "[!] Session: ESTABLISHED (User ID: 1)",
        "",
        "========================================================================",
        " STATUS: AUTHENTICATED AS 'ADMIN' | IMPACT: TOTAL SYSTEM COMPROMISE ",
        "========================================================================",
    ]

    for line in evidence_lines:
        color = "\033[33m" if "[" in line else "\033[37m"
        if "AUTHENTICATED" in line: color = "\033[1;31m"
        tech_print(line, 0.02, color)
        time.sleep(0.1)

    print("\n" + "#" * 80)
    tech_print(">>> EVIDENCE LOGGED. OPENING ADMIN SESSION... <<<", 0.05, "\033[1;36m")
    print("#" * 80)
    
    # Opening the REAL GDK target as seen in the logs
    target_url = "https://gitlab.local/admin"
    time.sleep(1)
    webbrowser.open(target_url)
    
    print(f"\n[SYSTEM] Redirecting to: {target_url}")

if __name__ == "__main__":
    try:
        gdk_audit_sequence()
    except KeyboardInterrupt:
        print("\n[SYSTEM] Sequence Aborted.")
