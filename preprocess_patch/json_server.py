import sys
import os
import argparse
import uuid
import time
import librosa
sys.path.append('waveglow/')
from pathlib import Path
import numpy as np
import torch
import time

from flask import Flask, request, Response
from flask_cors import CORS
from flask import render_template, jsonify, send_file

from audio import load_wav, save_wav
from hparams import create_hparams
from model import Tacotron2
from layers import TacotronSTFT, STFT
from audio_processing import griffin_lim
from train import load_model
from text import text_to_sequence
from denoiser import Denoiser

app = Flask(__name__)
CORS(app)

def plot_data(data, figsize=(16, 4)):
    fig, axes = plt.subplots(1, len(data), figsize=figsize)
    for i in range(len(data)):
        axes[i].imshow(data[i], aspect='auto', origin='bottom', 
                       interpolation='none')

@app.route('/test')
def test():
    return "hello world! this is ysh speak!"


@app.route('/demo')
def demo():
    return render_template('demo.html')

@app.route('/synthesize', methods=['GET', 'POST'])
def synthesize():
    t1 = time.time()
    text = request.values.get('text').strip()

    sequence = np.array(text_to_sequence(text, ['english_punctuation_cleaners']))[None, :]
    sequence = torch.autograd.Variable(torch.from_numpy(sequence)).cuda().long()

    print(f"preprocess time {time.time() - t1}")

    t2 = time.time()
    mel_outputs, mel_outputs_postnet, _, alignments = model.inference(sequence)
    
    with torch.no_grad():
        audio = waveglow.infer(mel_outputs_postnet, sigma=0.666)
    # ipd.Audio(audio[0].data.cpu().numpy(), rate=hparams.sampling_rate)
    print(f"inference time {time.time() - t2}")
    
    t3 = time.time()
    audio_denoised = denoiser(audio, strength=0.01)[:, 0]
    #ipd.Audio(audio_denoised.cpu().numpy(), rate=hparams.sampling_rate) 
    print(f"denoise time {time.time() - t3}")

    t4 = time.time()
    wav_name = f'{str(uuid.uuid1())}'
    whole_path = result_path /  f'{wav_name}.{ext}'
    librosa.output.write_wav(str(whole_path), audio_denoised.cpu().numpy().T, hparams.sampling_rate)
    print(f"save time {time.time() - t4}")
    print(f"total time {time.time() - t1}")
    print(f'input length {len(text)}, ratio {(time.time()-t1)/len(text)}')
    return send_file(whole_path, mimetype=f'audio/{ext}')

current_dir = Path(__file__).resolve().parent
result_path = current_dir /  'result'
os.makedirs(result_path, exist_ok=True)
ext = 'mp3'

hparams = create_hparams()
hparams.sampling_rate = 22050

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=8000)
    parser.add_argument('--hparams', default='', help='Hyperparameter overrides as a comma-separated list of name=value pairs')
    args = parser.parse_args()

    checkpoint_path = "model/tacotron2_statedict.pt"
    model = load_model(hparams)
    model.load_state_dict(torch.load(checkpoint_path)['state_dict'])
    _ = model.eval()

    waveglow_path = 'model/waveglow_old.pt'
    waveglow = torch.load(waveglow_path)['model']
    waveglow.cuda()
    denoiser = Denoiser(waveglow)

    print(f'Serving on port {args.port}')

    app.run(host="0.0.0.0", port=args.port)




