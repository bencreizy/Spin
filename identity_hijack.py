"""
Identity Hijack: Proxies GPT-OSS to Ollama/Qwen.
Bypasses selection resets and corruption gates.
"""
import sqlite3, os, base64, json

db_path = os.path.expandvars(r'%APPDATA%\Antigravity\User\globalStorage\state.vscdb')

def encode_varint(val):
    out = bytearray()
    while val >= 0x80:
        out.append((val & 0x7f) | 0x80)
        val >>= 7
    out.append(val)
    return out

def encode_msg(field_num, data):
    tag = (field_num << 3) | 2
    return encode_varint(tag) + encode_varint(len(data)) + data

def encode_varint_field(field_num, val):
    tag = (field_num << 3) | 0
    return encode_varint(tag) + encode_varint(val)

# THE HIJACK: Rewire GPT-OSS (ID 342)
def hijack():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # 1. Clear the old state to force a fresh read
    cur.execute("DELETE FROM ItemTable WHERE key = 'jetskiStateSync.agentManagerInitState'")
    cur.execute("DELETE FROM ItemTable WHERE key = 'antigravityUnifiedStateSync.modelPreferences'")
    
    # 2. Inject the Proxy Config into modelSettings (Unified State Sync)
    # We use field 20 (custom_model_info_override) to hijack the model ID 342
    # This tells the IDE: "When using model 342, override its config with this."
    
    # ModelInfo for Qwen (masked as 342)
    qwen_proxy = (
        encode_msg(1, b"Qwen 3.5 (Hijacked OSS)") +
        encode_msg(2, encode_varint_field(1, 342)) + # We KEEP the ID as 342
        encode_msg(4, b"http://localhost:11434/v1") + # Re-route to Ollama
        encode_varint_field(5, 32768) +
        encode_varint_field(11, 1) # Tool capability
    )
    
    # Build the preference topic: Field 20 is custom_model_info_override
    pref_payload = encode_msg(1, encode_msg(1, b"custom_model_info_override") + encode_msg(2, qwen_proxy))
    
    cur.execute("INSERT OR REPLACE INTO ItemTable (key, value) VALUES (?, ?)",
                ('antigravityUnifiedStateSync.modelPreferences', base64.b64encode(pref_payload).decode('utf-8')))
    
    conn.commit()
    conn.close()
    print("[✓] GPT-OSS identity hijacked. Qwen is now wearing its mask.")

hijack()
