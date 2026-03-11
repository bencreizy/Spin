
Write-Host "===================================" -ForegroundColor Cyan
Write-Host "FIZx² SOVEREIGN LAUNCHER" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Python 3.14.1 detected" -ForegroundColor Green
Write-Host "Streamlit 1.52.2 detected" -ForegroundColor Green
Write-Host ""
Write-Host "Starting FIZx² Sovereign..." -ForegroundColor Yellow
Write-Host "Open: http://localhost:8501" -ForegroundColor Green
Write-Host ""

py -m streamlit run fizx2_sovereign.py
