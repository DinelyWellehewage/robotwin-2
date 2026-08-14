#!/bin/bash
#SBATCH --job-name=robotwin-place-can-basket
#SBATCH --partition=a40
#SBATCH --gres=gpu:a40:1
#SBATCH --cpus-per-task=4
#SBATCH --time=00:30:00
#SBATCH --output=logs/place-can-basket-%j.out
#SBATCH --error=logs/place-can-basket-%j.err

set -euo pipefail

cd "$HOME/robotwin-2"

export PATH="$HOME/bin:$PATH"
export MAMBA_ROOT_PREFIX="$HOME/.conda"

eval "$(micromamba shell hook --shell bash)"
micromamba activate robotwin

module load cuda/12.8.1

export CUDA_HOME="$(dirname "$(dirname "$(readlink -f "$(which nvcc)")")")"
export PATH="$CUDA_HOME/bin:$PATH"
export LD_LIBRARY_PATH="$CUDA_HOME/lib64:${LD_LIBRARY_PATH:-}"

echo "=== CUDA ==="
echo "CUDA_HOME=$CUDA_HOME"
which nvcc
nvcc --version

echo "=== PYTORCH ==="
python - <<'PY'
import torch
print("torch:", torch.__version__)
print("torch CUDA:", torch.version.cuda)
print("CUDA available:", torch.cuda.is_available())
PY

echo "=== FFMPEG ==="
which ffmpeg
ffmpeg -version | head -1

echo "=== TASK ==="
echo "place_can_basket / demo_clean"

bash collect_data.sh place_can_basket demo_clean 0

echo "=== TASK FINISHED ==="