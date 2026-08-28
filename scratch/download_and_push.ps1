$dir = "C:\Users\FAIZAL RIDHO ILHAMI\.gemini\antigravity-ide\brain\e94c9e3e-4bf9-4ed7-a707-ee438f344fc8\scratch"
if (!(Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force }
$zipPath = Join-Path $dir "git-portable.exe"
$extractDir = Join-Path $dir "git"

# Clean up old extraction if it failed
if (Test-Path $extractDir) { Remove-Item $extractDir -Recurse -Force }

Write-Host "1. Downloading Portable Git..."
$url = "https://github.com/git-for-windows/git/releases/download/v2.42.0.windows.2/PortableGit-2.42.0.2-64-bit.7z.exe"
Invoke-WebRequest -Uri $url -OutFile $zipPath

Write-Host "2. Extracting Git (waiting for completion)..."
# Start process and wait for extraction to finish
$process = Start-Process -FilePath $zipPath -ArgumentList "-y", "-o`"$extractDir`"" -PassThru -Wait -NoNewWindow

Write-Host "3. Cleaning up zip..."
# Wait a bit just in case
Start-Sleep -Seconds 3
if (Test-Path $zipPath) { Remove-Item $zipPath -Force -ErrorAction SilentlyContinue }

$gitPath = Join-Path $extractDir "cmd\git.exe"
if (Test-Path $gitPath) {
    Write-Host "4. Git ready. Initializing and pushing..."
    Set-Location "c:\Users\FAIZAL RIDHO ILHAMI\Documents\pasis"
    & $gitPath init
    & $gitPath remote remove origin
    & $gitPath remote add origin https://github.com/ilhamrf540-ship-it/Staf-Renada.git
    & $gitPath add .
    & $gitPath commit -m "Update portal absensi dan ujian militer"
    & $gitPath branch -M main
    & $gitPath push -u origin main
    Write-Host "Push completed successfully!"
} else {
    Write-Host "Failed to prepare Git. Checked path: $gitPath"
}
