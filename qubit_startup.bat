@echo off
title Qubit Stability Core - Resonance 1.618
echo [!] Initializing Stability Layer...
:: Runs the Python stability engine in the background
start /B python qubit_stability_core.py > stability_log.txt 2>&1
echo [!] Integrating Qwen-Resonant-Core...
python qwen_integrator.py
echo [!] Verifying System Coherence...
python final_coherence.py
echo [!] System Resonant.
pause