import os
import subprocess


UPSTREAM_REPO = 'https://github.com/5hojib/new'
UPSTREAM_BRANCH = 'main'

if os.path.exists('.git'):
    run(["rm", "-rf", ".git"])

update = subprocess.run([
    f"git init -q && "
    f"git config --global user.email yesiamshojib@gmail.com && "
    f"git config --global user.name 5hojib && "
    f"git add . && "
    f"git commit -sm update -q && "
    f"git remote add origin {UPSTREAM_REPO} && "
    f"git fetch origin -q && "
    f"git reset --hard origin/{UPSTREAM_BRANCH} -q"
], shell=True)