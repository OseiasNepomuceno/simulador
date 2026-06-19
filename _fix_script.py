import subprocess, os

os.chdir('repo_simulador')
# Try git checkout
subprocess.run(['git', 'checkout', 'HEAD~1', '--', 'vagas/index.html'])
