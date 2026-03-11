"""
Restore agentManagerInitState to a clean state by removing our surgical injection.
"""
import sqlite3, os, base64

db_path = os.path.expandvars(r'%APPDATA%\Antigravity\User\globalStorage\state.vscdb')

def restore():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # We'll try to find a key that holds the default state. 
    # Usually, if we delete these, the IDE will re-sync them on start.
    keys_to_reset = [
        'jetskiStateSync.agentManagerInitState',
        'antigravityUnifiedStateSync.modelPreferences'
    ]
    
    for key in keys_to_reset:
        cur.execute("DELETE FROM ItemTable WHERE key = ?", (key,))
        print(f"[✓] Cleared {key} - IDE will re-sync defaults on next start.")
        
    conn.commit()
    conn.close()

restore()
