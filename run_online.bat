@echo off
chcp 65001 >nul
title UniMaster AI Pro v7.0 - CHE DO ONLINE TOAN CAU (HTTPS)
cd /d "%~dp0"

echo ====================================================================
echo   UNIMASTER AI PRO v7.0 - KHOI CHAY ONLINE TOAN CAU (MOI NOI 4G/5G)
echo ====================================================================
echo.

python start_online.py
pause
