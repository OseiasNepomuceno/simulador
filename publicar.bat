@echo off
echo ======================================
echo  COREGOV - Publicando nova Trilha do Conhecimento
echo ======================================
echo.
cd /d "C:\Users\oseia\.picoclaw\workspace\repo_simulador"
echo Fazendo push para o GitHub...
git push origin main
echo.
if %ERRORLEVEL% EQU 0 (
    echo ✅ Pagina publicada com sucesso!
    echo Acesse: https://coregov.com.br/trilha.html
) else (
    echo ❌ Erro ao publicar. Tente manualmente:
    echo    cd C:\Users\oseia\.picoclaw\workspace\repo_simulador
    echo    git push origin main
)
pause
