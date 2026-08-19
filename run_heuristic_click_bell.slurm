#!/bin/bash
#SBATCH --job-name=heuristic-click-bell
#SBATCH --partition=a40
#SBATCH --gres=gpu:a40:1
#SBATCH --cpus-per-task=4
#SBATCH --time=00:10:00
#SBATCH --output=logs/heuristic-click-bell-%j.out
#SBATCH --error=logs/heuristic-click-bell-%j.err

set -euo pipefail

cd "$HOME/robotwin-2"

export PATH="$HOME/bin:$PATH"

module load cuda/12.8.1

export CUDA_HOME="$(dirname "$(dirname "$(readlink -f "$(which nvcc)")")")"
export PATH="$CUDA_HOME/bin:$PATH"
export LD_LIBRARY_PATH="$CUDA_HOME/lib64:${LD_LIBRARY_PATH:-}"

echo "=== NODE ==="
hostname

echo "=== GPU ==="
nvidia-smi --query-gpu=name --format=csv,noheader

echo "=== HEURISTIC TEST ==="
micromamba run -n robotwin python -m heuristic_policies.run_click_bell_policy "$1"

echo "=== FINISHED ==="
