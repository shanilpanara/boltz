#!/bin/bash
# Check input folder as $1
INPUT_FOLDER=$1
if [ -z "$INPUT_FOLDER" ]; then
    echo "Input folder with all the YAMLsis required."
    echo "Usage: $0 <input_folder>"
    exit 1
fi

source ~/programs/boltz/.venv/bin/activate
boltz predict $INPUT_FOLDER/ \
    --no_kernels \
    --diffusion_samples 5 \
    --recycling_steps 10 \
    --output_format pdb \
    --out_dir results # \
    # --step_scale 1.3