#!/bin/bash
#SBATCH --job-name=heuristic-eval
#SBATCH --partition=a40
#SBATCH --gres=gpu:a40:1
#SBATCH --cpus-per-task=4
#SBATCH --time=00:30:00
#SBATCH --output=logs/heuristic-eval-%j.out
#SBATCH --error=logs/heuristic-eval-%j.err

set -euo pipefail

if [ "$#" -ne 3 ]; then
    echo "Usage:"
    echo "  sbatch run_heuristic_evaluator.slurm TASK_NAME POLICY_PATH OUTPUT_PATH"
    echo
    echo "Example:"
    echo "  sbatch run_heuristic_evaluator.slurm click_bell /path/to/policy.py /path/to/result.json"
    exit 2
fi

TASK_NAME="$1"
POLICY_PATH="$2"
OUTPUT_PATH="$3"

cd "$HOME/robotwin-2"

export PATH="$HOME/bin:$HOME/.local/bin:$PATH"

module load cuda/12.8.1

echo "=== HEURISTIC SEARCH EVALUATION ==="
echo "Task: ${TASK_NAME}"
echo "Policy: ${POLICY_PATH}"
echo "Seed set: search (0-9)"
echo "Output: ${OUTPUT_PATH}"
echo "Node: $(hostname)"

micromamba run -n robotwin python \
    -m heuristic_learning.evaluator.evaluate_candidate \
    --task "${TASK_NAME}" \
    --policy "${POLICY_PATH}" \
    --output "${OUTPUT_PATH}"

echo "=== FINISHED ==="
