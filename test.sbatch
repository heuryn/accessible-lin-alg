#!/bin/bash
#SBATCH --job-name=model_test
#SBATCH --output=logs/test_%j.out
#SBATCH --error=logs/test_%j.err
#SBATCH --time=00:10:00
#SBATCH --gres=gpu:H100:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=64G

mkdir -p logs

module load cuda/12

uv run test.py
