#!/bin/bash
#SBATCH --job-name=robotwin-test
#SBATCH --partition=a40
#SBATCH --gres=gpu:a40:1
#SBATCH --cpus-per-task=4
#SBATCH --time=01:00:00
#SBATCH --output=logs/robotwin-%j.out
#SBATCH --error=logs/robotwin-%j.err

set -euo pipefail

cd "$HOME/robotwin-2"

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

echo "=== INSTALL ==="
bash scripts/_install.sh