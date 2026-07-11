@echo off
cd /d C:\Users\oseia\.picoclaw\workspace\repo_simulador
git add produtos/calendario-sudeste.html produtos/calendario-sul.html produtos/regioes/centro-oeste.html
if %errorlevel% equ 0 (
    git commit -m "Remove 'CNPJ em regularizacao' do footer - CNPJ ativo desde mar/2026"
    if %errorlevel% equ 0 (
        git push
        echo PRONTO! Commit e push realizados com sucesso.
    )
)
