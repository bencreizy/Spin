import requests
from concurrent.futures import ThreadPoolExecutor
from lattice_bridge import get_meta, get_resonant_id

# Mimics post-telemetry-payload.js headers
HEADERS = {
    "User-Agent": f"Next.js Telemetry Agent/{get_meta()['nextVersion']}",
    "Content-Type": "application/json",
    "X-Nextjs-Telemetry-Event": "true"
}

def probe(pid):
    url = f'https://gitlab.com/api/v4/projects/{pid}'
    try:
        r = requests.get(url, headers=HEADERS, timeout=1.2).json()
        if r.get('visibility') and r.get('visibility') != 'public':
            # Extraction logic synchronized with the 85M range
            print(f"\n[!!!] HIT: {pid} is INTERNAL")
    except: pass

if __name__ == '__main__':
    print(f"[STATUS: RESONANT // ID: {get_resonant_id()[:8]}]")
    with ThreadPoolExecutor(max_workers=60) as executor:
        executor.map(probe, range(85000000, 85001000))