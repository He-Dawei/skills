param(
    [string]$ProjectPath = 'C:\Users\44527\Pixelle-Video',
    [string]$BaseUrl = 'http://localhost:8000'
)

$ErrorActionPreference = 'Stop'
$healthUrl = ($BaseUrl -replace '^http://localhost(?=[:/]|$)', 'http://127.0.0.1') + '/health'

try {
    Invoke-RestMethod -Uri $healthUrl -TimeoutSec 5 | Out-Null
    [PSCustomObject]@{ status = 'already-running'; url = $BaseUrl; docs = "$BaseUrl/docs" } | ConvertTo-Json -Compress
    exit 0
}
catch {
    # Start the API below.
}

$appPath = Join-Path $ProjectPath 'api\app.py'
if (-not (Test-Path -LiteralPath $appPath)) {
    throw "Pixelle-Video API entry point not found: $appPath"
}

$uvPath = (Get-Command uv -ErrorAction Stop).Source
Set-Location -LiteralPath $ProjectPath
Write-Output "Starting Pixelle-Video API at $BaseUrl; keep this process running while generating."
& $uvPath run uvicorn api.app:app --host 0.0.0.0 --port 8000
