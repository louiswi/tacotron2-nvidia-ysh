Enviorment Requirements:
1. pip install -r requirements.txt
2. install pytorch 1.0 according to your CUDA version (https://pytorch.org/get-started/previous-versions/)

Possible Error:
1.  ModuleNotFoundError: No module named 'denoiser'
    Solution: 
    1.  in root dir run: `git submodule init; git submodule update`
    2.  in `waveglow` dir run: `git pull origin master; git checkout 6188a1d106a1060336040db82f464d6441f39e21`

2.  AttributeError: 'ConvTranspose1d' object has no attribute 'padding_mode'
    Solution: make sure you installed the pytorch 1.0

3.  RuntimeError: cuDNN error: CUDNN_STATUS_EXECUTION_FAILED
    Solution: make sure you installed the pytorch 1.0 according to your cuda version, for example, for machine using CUDA10 should install pytorch with:
    `conda install pytorch==1.0.0 torchvision==0.2.1 cuda100 -c pytorch`


How to Use:
    1.  change in the run.sh to activate your enviorment
    2.  go to broswer at `localhost:8000/demo` to use the demo page
    3.  you can also call the REST API with `localhost:8000/synthesize?text=TEXT_TO_SYNTHESIZE`, replace TEXT_TO_SYNTHESIZE with what you want to synthesize.


Tips:
1.  remember to add stop sign in the end of sentence, or the model may not know when to stop.
2.  the generated mp3 file will be stored in the `result` dir.
3.  the model has a limit of input length, if your sentence is too long and be truncated, try to split them to smaller parts and synthesize each by each.

convert_mp3_patch:
add `save_mp3_use_ffmpeg` function in audio.py, need ffmpeg installed on the host machine, if failed, will return the input wav_file
add ext and mp3 bitrate choice in the json_server.py