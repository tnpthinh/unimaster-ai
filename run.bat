@echo off
title UniMaster AI - He Thong On Thi Dai Hoc Sieu Cap VIP PRO
cd /d "%~dp0"

echo ========================================================
echo   UNIMASTER AI - HE THONG ON THI DAI HOC SIEU CAP VIP PRO
echo ========================================================
echo.
echo Dang khoi dong may chu tai http://localhost:8080 ...
echo Dang mo trinh duyet...

start http://localhost:8080
python server.py
pause
