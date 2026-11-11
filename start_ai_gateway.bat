@echo off
chcp 65001 >nul
cd /d "%~dp0"
title UniMaster AI Gateway - 9Router

echo ================================================
echo   UniMaster AI Gateway
echo ================================================
echo.

echo [1/4] Kiem tra Python...
python --version >nul 2>&1
if errorlevel 1 (
  echo   LOI: Chua cai Python hoac chua co trong PATH.
  echo   Tai tai: https://www.python.org/downloads/
  echo   Nho tick "Add Python to PATH" khi cai.
  pause
  exit /b 1
)
echo   OK

echo.
echo [2/4] Kiem tra 9Router o cong 20128...
powershell -NoProfile -Command "try { $r = Invoke-WebRequest -UseBasicParsing -TimeoutSec 3 'http://127.0.0.1:20128/v1/models'; if ($r.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }"
if errorlevel 1 (
  echo   Chua chay - dang tu khoi dong 9Router...
  where 9router >nul 2>&1
  if errorlevel 1 (
    echo   LOI: Khong tim thay lenh 9router.
    echo   Hay cai bang lenh: npm install -g 9router
    pause
    exit /b 1
  )
  start "9Router Server" /min cmd /c "9router -n"
  echo   Dang cho 9Router san sang...
  powershell -NoProfile -Command "$ok=$false; for ($i=0; $i -lt 40; $i++) { try { $r = Invoke-WebRequest -UseBasicParsing -TimeoutSec 2 'http://127.0.0.1:20128/v1/models'; if ($r.StatusCode -eq 200) { $ok=$true; break } } catch {}; Start-Sleep -Milliseconds 700 }; if ($ok) { exit 0 } else { exit 1 }"
  if errorlevel 1 (
    echo   LOI: 9Router khong khoi dong duoc sau 28 giay.
    echo   Hay mo 9Router bang tay roi chay lai file nay.
    pause
    exit /b 1
  )
)
echo   OK - 9Router dang chay

echo.
echo [3/4] Khoi dong gateway + Cloudflare Tunnel...
python start_ai_gateway.py
if errorlevel 1 (
  echo.
  echo   LOI: Gateway khong khoi dong duoc. Xem log trong ai_gateway.log
  pause
  exit /b 1
)

echo.
echo [4/4] Hoan tat. Gateway chay nen - co the dong cua so nay.
echo.
echo   Kiem tra lai bat cu luc nao: bam dup file nay lan nua.
echo   Tat gateway:                python start_ai_gateway.py --stop
echo.
pause
