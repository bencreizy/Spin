import sys
import requests
import webbrowser
from concurrent.futures import ThreadPoolExecutor
from lattice_bridge import get_meta, get_resonant_id

def probe(pid):
    url = f'https://gitlab.com/api/v4/projects/{pid}'
    headers = {
        'User-Agent': f'Next.js Telemetry Agent/{get_meta()["nextVersion"]}',
        'X-Nextjs-Telemetry-Event': 'true'
    }
    try:
        r = requests.get(url, headers=headers, timeout=1.2).json()
        if r.get('visibility') and r.get('visibility') != 'public':
            print(f'\n[!!!] HIT: {pid} is INTERNAL')
            with open('bounty_loot.txt', 'a') as f:
                f.write(f'ID: {pid} | URL: {url}\n')
            webbrowser.open(url)
    except: pass

if __name__ == '__main__':
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 85000000
    end = int(sys.argv[2]) if len(sys.argv) > 2 else 85010000
    print(f'[SYSTEM STATUS: RESONANT // ID: {get_resonant_id()[:8]}]')
    print(f'Vulnerability Mapping Active: {start} to {end}')
    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(probe, range(start, end))
