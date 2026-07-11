@echo off
cd /d C:\Users\oseia\.picoclaw\workspace\repo_simulador
echo === Salvando alteracoes temporarias ===
git stash
echo === Puxando mudancas do remoto ===
git pull --rebase
if %errorlevel% neq 0 (
    echo ERRO no pull.
    git stash pop
    exit /b 1
)
echo === Restaurando alteracoes ===
git stash pop
echo === Enviando para o GitHub ===
git push
if %errorlevel% equ 0 (
    echo PRONTO! Tudo sincronizado!
) else (
    echo ERRO no push.
)
