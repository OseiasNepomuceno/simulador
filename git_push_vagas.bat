@echo off
cd /d %~dp0
git add vagas/index.html
if %errorlevel% equ 0 (echo [OK] git add) else (echo [FAIL] git add & exit /b %errorlevel%)
git commit -m "remove planos de acesso - todas as vagas ficam visiveis sem restricao"
if %errorlevel% equ 0 (echo [OK] git commit) else (echo [FAIL] git commit & exit /b %errorlevel%)
git push origin main
if %errorlevel% equ 0 (echo [OK] git push) else (echo [FAIL] git push & exit /b %errorlevel%)
echo === ALL DONE ===
