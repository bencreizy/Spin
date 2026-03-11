import os
import platform
import hashlib

def get_resonant_id():
    # Mimics project-id.js: Hash the CWD as a project anchor
    raw_id = os.getcwd()
    salt = "bountylab_v1_1.618" 
    return hashlib.sha256((raw_id + salt).encode()).hexdigest()

def get_meta():
    # Mimics anonymous-meta.js: Extracts system 'traits'
    return {
        "systemPlatform": platform.system().lower(),
        "systemRelease": platform.release(),
        "systemArchitecture": platform.machine(),
        "nextVersion": "15.5.9", # Matches source
        "isCI": False
    }