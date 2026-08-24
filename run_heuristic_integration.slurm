#!/bin/bash
#SBATCH --job-name=heuristic-integration
#SBATCH --partition=a40
#SBATCH --gres=gpu:a40:1
#SBATCH --cpus-per-task=4
#SBATCH --time=00:15:00
#SBATCH --output=logs/heuristic-integration-%j.out
#SBATCH --error=logs/heuristic-integration-%j.err

set -euo pipefail

if [ "$#" -ne 4 ]; then
    echo "Usage:"
    echo "  sbatch run_heuristic_integration.slurm TASK_NAME POLICY_PATH OUTPUT_PATH SEED"
    exit 2
fi

TASK_NAME="$1"
POLICY_PATH="$2"
OUTPUT_PATH="$3"
SEED="$4"

cd "$HOME/robotwin-2"

export PATH="$HOME/bin:$HOME/.local/bin:$PATH"

module load cuda/12.8.1

echo "=== HEURISTIC INTEGRATION TEST ==="
echo "Task: ${TASK_NAME}"
echo "Policy: ${POLICY_PATH}"
echo "Integration seed: ${SEED}"
echo "Output: ${OUTPUT_PATH}"
echo "Node: $(hostname)"

micromamba run -n robotwin python \
    -m heuristic_learning.evaluator.evaluate_candidate \
    --task "${TASK_NAME}" \
    --policy "${POLICY_PATH}" \
    --output "${OUTPUT_PATH}" \
    --integration-seed "${SEED}"

echo "=== FINISHED ==="
