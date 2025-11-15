#!/usr/bin/env bash
set -euo pipefail

echo "Downloading marinecircuits/kicad-template"

# Create a temp directory and download the template tarball
TMPDIR=$(mktemp -d)
curl -sSL https://github.com/marinecircuits/kicad-template/archive/refs/heads/main.tar.gz \
    | tar -xz -C "$TMPDIR" --strip-components=1

echo "Copying template files into current directory"
cp -R "$TMPDIR"/. .

rm -rf "$TMPDIR"

# Python environment
echo "Creating Python virtual environment (.venv)"
python3 -m venv .venv

echo "Installing Python dependencies"
source .venv/bin/activate
pip install -r requirements.txt

# Setup script
echo "Running KiCad template setup"
python3 scripts/setup_template.py

# Git
if [ ! -d .git ]; then
    echo "Initializing Git repository"
    git init .
fi

git add .

# Pre-commit
echo "Installing pre-commit hook (commit-msg)"
pre-commit install --hook-type commit-msg

echo
echo "Project is ready"
echo
