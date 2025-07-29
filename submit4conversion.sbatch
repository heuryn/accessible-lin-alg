#!/bin/bash
#SBATCH --job-name=latex2html
#SBATCH --output=logs/latex2html_%j.out
#SBATCH --error=logs/latex2html_%j.err
#SBATCH --time=04:00:00
#SBATCH --gres=gpu:H100:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=160G

# Create log and output directories if they don't exist
mkdir -p logs
mkdir -p chapter1

# Load required modules (adjust for your cluster)
module load cuda/12

# Run the Python conversion script
uv run latex2html.py
