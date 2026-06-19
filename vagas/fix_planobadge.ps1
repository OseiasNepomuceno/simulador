$file = "C:\Users\oseia\.picoclaw\workspace\repo_simulador\vagas\index.html"
$content = Get-Content $file -Raw

# Remove the linha ${planoBadge} do template
$content = $content -replace '                    \$\{novoLabel\}\r\n                    \$\{planoBadge\}\r\n', '                    ${novoLabel}`r`n'

Set-Content $file $content -NoNewline
Write-Output "Done"
