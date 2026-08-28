@echo off
echo Menginisialisasi Git...
git init
git remote remove origin 2>nul
git remote add origin https://github.com/ilhamrf540-ship-it/Staf-Renada.git
git add .
git commit -m "Update portal absensi dan ujian militer"
echo Melakukan Push ke Github...
git branch -M main
git push -u origin main
echo Selesai!
pause
