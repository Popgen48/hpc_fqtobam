#! /bin/bash
#SBATCH -J fq2bam
#SBATCH -o ./slurm/%x.%j.%N.out
#SBATCH -D ./
#SBATCH --get-user-env
#SBATCH --clusters=serial
#SBATCH --partition=serial_std
#SBATCH --cpus-per-task=14
#SBATCH --time=94:00:00
#SBATCH --export=NONE
#SBATCH --mail-type=END
