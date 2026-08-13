#!/bin/bash
#SBATCH --job-name=robotwin-install
#SBATCH --partition=a40
#SBATCH --gres=gpu:a40:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --output=logs/robotwin-install-%j.out
#SBATCH --error=logs/robotwin-install-%j.err

set -e

cd "$HOME/robotwin-2"
mkdir -p logs

export PATH="$HOME/bin:$PATH"
eval "$(micromamba shell hook --shell bash)"
micromamba activate robotwin

module load cuda/12.8.1

echo "=== NODE ==="
hostname

echo "=== GPU ==="
nvidia-smi

echo "=== PYTHON ==="
python --version
which python

echo "=== INSTALL ROBOTWIN ==="
bash scripts/_install.sh