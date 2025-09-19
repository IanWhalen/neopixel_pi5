#!/bin/sh
cd `dirname $0`

sudo apt-get update
sudo apt-get install -y python3.11-dev

# Create a virtual environment to run our code
VENV_NAME="venv"
PYTHON="$VENV_NAME/bin/python"

if ! $PYTHON -m pip install pyinstaller -Uqq; then
    exit 1
fi

$PYTHON -m PyInstaller --onefile --hidden-import="googleapiclient" src/main.py
tar -czvf dist/archive.tar.gz meta.json ./dist/main
