import subprocess, os

# Already inside repo_simulador
subprocess.run(['git', 'add', 'produtos/calendario-sudeste.html', 'produtos/calendario-sul.html', 'produtos/regioes/centro-oeste.html'], check=True)
print("Added files")

subprocess.run(['git', 'commit', '-m', "Remove 'CNPJ em regularizacao' do footer - CNPJ ativo desde mar/2026"], check=True)
print("Committed")

subprocess.run(['git', 'push'], check=True)
print("Pushed!")
