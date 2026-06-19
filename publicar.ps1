# Script para publicar a nova Trilha do Conhecimento
# Execute no PowerShell

Write-Host "🚀 Publicando nova Trilha do Conhecimento COREGOV..." -ForegroundColor Green
Set-Location "C:\Users\oseia\.picoclaw\workspace\repo_simulador"

git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ Publicado com sucesso!" -ForegroundColor Green
    Write-Host "Acesse: https://coregov.com.br/trilha.html" -ForegroundColor Cyan
} else {
    Write-Host "`n❌ Erro no push. Tente manualmente:" -ForegroundColor Red
    Write-Host "   cd C:\Users\oseia\.picoclaw\workspace\repo_simulador" -ForegroundColor Yellow
    Write-Host "   git push origin main" -ForegroundColor Yellow
}
