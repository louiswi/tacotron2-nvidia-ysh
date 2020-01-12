#!/bin/bashsh 
source /home/shihangyu/Bin/anaconda3/etc/profile.d/conda.sh
conda activate tacotron2-nvidia
#gunicorn -w 4 json_server:app -b 0.0.0.0:8000
CUDA_VISIBLE_DEVICES=0 python json_server.py --port 8000
