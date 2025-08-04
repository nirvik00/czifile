import os
import subprocess
print(os.getcwd())
result = subprocess.run(
    ['git', 'init'],
    cwd= os.getcwd(), 
    capture_output=True,
    text=True
)
print(result.stdout)

result = subprocess.run(
    ['git', 'add', '.'],
    cwd= os.getcwd(), 
    capture_output=True,
    text=True
)
print(result.stdout)

x = input('commit message')
result = subprocess.run(
    ['git', 'commit', '-m', str(x)],
    cwd= os.getcwd(), 
    capture_output=True,
    text=True
)
print(result.stdout)

res = subprocess.run(['git', 'push', 'origin', 'main'], cwd=os.getcwd(), capture_output=True, text=True)
print(result.stdout)