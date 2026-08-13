#!/bin/bash
#SBATCH --job-name=robotwin-test
#SBATCH --partition=a40
#SBATCH --gres=gpu:a40:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --output=logs/robotwin-%j.out
#SBATCH --error=logs/robotwin-%j.err

set -e

cd "$HOME/RoboTwin"

module load cuda/12.8.1

# Activate your environment here once created
# source ~/miniconda3/etc/profile.d/conda.sh
# conda activate RoboTwin

hostname
nvidia-smi
python --version

# Later replace this with the actual RoboTwin command
# python ...