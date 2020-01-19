import sys
import os
import argparse
import uuid
import re
import librosa
sys.path.append('waveglow/')
from pathlib import Path
import numpy as np
import torch
import time

from flask import Flask, request, after_this_request
from flask_cors import CORS
from flask import render_template, send_file

from audio import save_mp3_use_ffmpeg
from hparams import create_hparams

from train import load_model
from text import text_to_sequence
from denoiser import Denoiser

from mylogger import logger

app = Flask(__name__)
CORS(app)

def np_pad_concate(a,b):
    max_len = max(a.shape[1], b.shape[1])

    a = np.pad(a[0],(0,max_len-a.shape[1]),'constant', constant_values=(0,0))
    b = np.pad(b[0],(0,max_len-b.shape[1]),'constant', constant_values=(0,0))
    a = np.expand_dims(a, 0)
    b = np.expand_dims(b, 0)
    c = np.concatenate([a,b], axis=0)

    return c

@app.route('/test')
def test():
    return "hello world! this is ysh speak!"


@app.route('/demo')
def demo():
    return render_template('demo.html')

@app.route('/synthesize', methods=['GET', 'POST'])
def synthesize():
    t1 = time.time()
    # cut the longer syntax, can stop memory grow
    text = request.values.get('text')[:200].strip()
    logger.info(f'input text: {text}')

    sequence = np.array(text_to_sequence(text, ['enhanced_english_cleaners'], verbose=True))[None, :]
    sequence = torch.autograd.Variable(torch.from_numpy(sequence)).cuda().long()

    torch.cuda.synchronize()
    t2 = time.time()
    logger.debug(f"preprocess time {t2 - t1}")

    try:
        with torch.no_grad():
            mel_outputs_postnet = model.inference_simple(sequence)
            torch.cuda.empty_cache()
            audio = waveglow.infer(mel_outputs_postnet, sigma=0.666)
            torch.cuda.empty_cache()

            torch.cuda.synchronize()
            t3 = time.time()
            logger.debug(f"inference time {t3 - t2}")

            audio_denoised = denoiser(audio, strength=0.01)[:, 0]

            torch.cuda.synchronize()
            t4 = time.time()
            logger.debug(f"denoise time {t4 - t3}")

    except RuntimeError as e:
        if e.args[0].startswith('CUDA out of memory'):
            logger.fatal('GPU OUT OF MEMORY!')

        torch.cuda.empty_cache()
        return None

    wav_name = f'{str(uuid.uuid1())}'
    whole_path_wav = result_path /  f'{wav_name}.wav'
    librosa.output.write_wav(str(whole_path_wav), audio_denoised.cpu().numpy().T, hparams.sampling_rate)

    if ext == 'wav':
        whole_path_ext = whole_path_wav
    elif ext == 'mp3':
        whole_path_ext = result_path /  f'{wav_name}.mp3'
        # if convert fail, return name fall back to whole_path_wav
        whole_path_ext = save_mp3_use_ffmpeg(hparams.sampling_rate, mp3_bitrate, whole_path_wav, whole_path_ext)
    else:
        return RuntimeError("unknown file extension")

    torch.cuda.synchronize()
    logger.debug(f"save time {time.time() - t4}")
    logger.debug(f"total time {time.time() - t1}")
    logger.debug(f'input length {len(text)}, ratio {(time.time()-t1)/len(text)}')

    @after_this_request
    def remove_file(response):
        torch.cuda.empty_cache()
        try:
            os.remove(whole_path_wav)
        except Exception as error:
            logger.error(f"Error removing file {whole_path_wav}")

        if ext != 'wav':
            try:
                os.remove(whole_path_ext)
            except Exception as error:
                logger.error(f"Error removing file {whole_path_ext}")

        return response

    return send_file(whole_path_ext, mimetype=f'audio/{ext}')

# split and synthesize for the long sentence, only use in experiment
@app.route('/synthesize_split', methods=['GET', 'POST'])
def synthesize_split():
    def split(long_text):
        return re.findall(r'.{1,100}(?:\s+|$)', long_text)

    t1 = time.time()
    # cut the longer syntax, can stop memory grow
    long_text = request.values.get('text').strip()
    logger.info(f'input text: {long_text}')

    text_list = split(long_text)

    audio_denoised_list = []

    for text in text_list:
        sequence = np.array(text_to_sequence(text, ['enhanced_english_cleaners'], verbose=True))[None, :]
        sequence = torch.autograd.Variable(torch.from_numpy(sequence)).cuda().long()

        torch.cuda.synchronize()
        t2 = time.time()
        logger.debug(f"preprocess time {t2 - t1}")

        try:
            with torch.no_grad():
                mel_outputs_postnet = model.inference_simple(sequence)
                torch.cuda.empty_cache()
                audio = waveglow.infer(mel_outputs_postnet, sigma=0.666)
                torch.cuda.empty_cache()

                torch.cuda.synchronize()
                t3 = time.time()
                logger.debug(f"inference time {t3 - t2}")

                audio_denoised = denoiser(audio, strength=0.01)[:, 0]

                torch.cuda.synchronize()
                t4 = time.time()
                logger.debug(f"denoise time {t4 - t3}")

        except RuntimeError as e:
            if e.args[0].startswith('CUDA out of memory'):
                logger.fatal('GPU OUT OF MEMORY!')

            torch.cuda.empty_cache()
            return None

        audio_denoised_list.append(audio_denoised)

    audio_denoised_long = torch.cat((audio_denoised_list), 1) # concatenate all the splited audios
    wav_name = f'{str(uuid.uuid1())}'
    whole_path_wav = result_path /  f'{wav_name}.wav'
    librosa.output.write_wav(str(whole_path_wav), audio_denoised_long.cpu().numpy().T, hparams.sampling_rate)

    if ext == 'wav':
        whole_path_ext = whole_path_wav
    elif ext == 'mp3':
        whole_path_ext = result_path /  f'{wav_name}.mp3'
        # if convert fail, return name fall back to whole_path_wav
        whole_path_ext = save_mp3_use_ffmpeg(hparams.sampling_rate, mp3_bitrate, whole_path_wav, whole_path_ext)
    else:
        return RuntimeError("unknown file extension")

        torch.cuda.synchronize()
        logger.debug(f"save time {time.time() - t4}")
        logger.debug(f"total time {time.time() - t1}")
        logger.debug(f'input length {len(text)}, ratio {(time.time()-t1)/len(text)}')

    @after_this_request
    def remove_file(response):
        torch.cuda.empty_cache()
        try:
            os.remove(whole_path_wav)
        except Exception as error:
            logger.error(f"Error removing file {whole_path_wav}")

        if ext != 'wav':
            try:
                os.remove(whole_path_ext)
            except Exception as error:
                logger.error(f"Error removing file {whole_path_ext}")

        return response

    return send_file(whole_path_ext, mimetype=f'audio/{ext}')



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=8000)
    parser.add_argument('--hparams', default='',
                        help='Hyperparameter overrides as a comma-separated list of name=value pairs')
    parser.add_argument('--ext', default='mp3', choices=["wav", "mp3"],
                        help='file save extension')
    parser.add_argument('--mp3_bitrate', default='48k', choices=['24k', '48k', '96k', '192k', '256k'],
                        help='mp3 bitrate, only useful when saved as mp3')
    args = parser.parse_args()

    current_dir = Path(__file__).resolve().parent
    result_path = current_dir / 'result'
    os.makedirs(result_path, exist_ok=True)

    ext = args.ext
    mp3_bitrate = args.mp3_bitrate

    hparams = create_hparams()
    hparams.sampling_rate = 22050


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




