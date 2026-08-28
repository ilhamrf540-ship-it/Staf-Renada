@echo off
echo Menginisialisasi Git menggunakan Portable Git...
set GIT_PATH="C:\Users\FAIZAL RIDHO ILHAMI\.gemini\antigravity-ide\brain\e94c9e3e-4bf9-4ed7-a707-ee438f344fc8\scratch\git\cmd\git.exe"
%GIT_PATH% init
%GIT_PATH% remote remove origin 2>nul
%GIT_PATH% remote add origin https://github.com/ilhamrf540-ship-it/Staf-Renada.git
%GIT_PATH% add .
%GIT_PATH% commit -m "Update portal absensi dan ujian militer"
echo Melakukan Push ke Github...
%GIT_PATH% branch -M main
%GIT_PATH% push -u origin main
echo Selesai!
pause
