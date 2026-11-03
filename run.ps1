Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  Starting Innovision NIT Rourkela 2026 Local Server" -ForegroundColor Green
Write-Host "  Open your browser at: http://localhost:3000" -ForegroundColor Yellow
Write-Host "========================================================" -ForegroundColor Cyan
Set-Location -Path $PSScriptRoot
node server.js

