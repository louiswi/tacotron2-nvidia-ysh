#!/usr/bin/env python
# coding: utf-8

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import argparse
import os
import sys
import re
sys.path.append('waveglow/')
import numpy as np
import torch

from hparams import create_hparams
from model import Tacotron2
from layers import TacotronSTFT, STFT
from audio_processing import griffin_lim
from train import load_model
from text import text_to_sequence
from denoiser import Denoiser

from scipy.io import wavfile


texts = [
	# From July 8, 2017 New York Times:
	'Scientists at the CERN laboratory say they have discovered a new particle.',
	'There\'s a way to measure the acute emotional intelligence that has never gone out of style.',
	'President Trump met with other leaders at the Group of 20 conference.',
	'The Senate\'s bill to repeal and replace the Affordable Care Act is now imperiled.',
	# From Google's Tacotron example page:
	'Generative adversarial network or variational auto-encoder.',
	'Basilar membrane and otolaryngology are not auto-correlations.',
	'He has read the whole thing.',
	'He reads books.',
	'He thought it was time to present the present.',
	'Thisss isrealy awhsome.',
	'The big brown fox jumps over the lazy dog.',
	'Did the big brown fox jump over the lazy dog?',
	"Peter Piper picked a peck of pickled peppers. How many pickled peppers did Peter Piper pick?",
	"She sells sea-shells on the sea-shore. The shells she sells are sea-shells I'm sure.",
	"Tajima Airport serves Toyooka.",
	#From The web (random long utterance)
	# 'On offering to help the blind man, the man who then stole his car, had not, at that precise moment, had any evil intention, quite the contrary, \
	# what he did was nothing more than obey those feelings of generosity and altruism which, as everyone knows, \
	# are the two best traits of human nature and to be found in much more hardened criminals than this one, a simple car-thief without any hope of advancing in his profession, \
	# exploited by the real owners of this enterprise, for it is they who take advantage of the needs of the poor.',
	# A final Thank you note!
	'Thank you so much for your support!',
	'Welcome to the inception institute of artificial intelligence, this is Tony Robbins, I am kidding, this is not really Tony Robbins, this is a computer generated voice, I am still a work in progress so do not mind any strange artifacts that you hear.',


	#yshlabel-test
    "the most powerful thing that has consequence in your life though is the thing we talk about, so often but I gotta say it again, and that is what's really ultimately shaping our lives our decisions.",
    "I want to put myself in line in a relationship or my business or my vision to make a difference in the world.",
    "every one of us has been put here, every one of us is unique and different and special.",
    "but it's true, never in the history of the world of things change so rapidly, so you need to find something that's eternal inside of yourself.",

    #yshlabel-train
    "when I ask most people this question what do you want they give me answers like well I know what I go on I don't want to live this way anymore I don't want to feel like hell anymore, that's not gonna give you what you want.",
    "and I got a phone call on the phone call was， that they've done additional tests and they found out that the cancer had spread throughout his spine and into his brain.",
    "this is happening because I'm just destined to fail.",
    "as they're allowed when I pinch myself I said how cool now I get to do a gig for Aerosmith, I'm not out there rock and rolling but sort of I am, I'm working with the rock and roller so it's fun so my point is maybe you're not doing what you originally envisioned, but maybe you'll find a way to do it even better if you have some faith.",
	]


def plot_data(data, _title, figsize=(16, 4)):
    fig, axes = plt.subplots(1, len(data), figsize=figsize)
    for i in range(len(data)):
        axes[i].imshow(data[i], aspect='auto', origin='bottom', 
                       interpolation='none')
    plt.savefig(_title)
    plt.cla()


args_parser = argparse.ArgumentParser()
args_parser.add_argument('--checkpoint_dir')
args_parser.add_argument('--name', required=True)
args = args_parser.parse_args()


inference_output = os.path.join('inference_output', args.name)
os.makedirs(inference_output, exist_ok=True)

hparams = create_hparams()
hparams.sampling_rate = 22050


checkpoint_dir = args.checkpoint_dir
checkpoint_paths = os.listdir(checkpoint_dir)
checkpoint_paths = [os.path.join(checkpoint_dir, item) for item in checkpoint_paths if re.match('checkpoint_(\d+)', item)]
checkpoint_paths = sorted(checkpoint_paths, key=lambda x:int(x.split('_')[-1]))
checkpoint_paths = checkpoint_paths[::-1]
# checkpoint_path = "model/tacotron2_statedict.pt"


waveglow_path = 'model/waveglow_old.pt'
waveglow = torch.load(waveglow_path)['model']
waveglow.cuda()
denoiser = Denoiser(waveglow)


model = load_model(hparams)
for i_checkpoint, checkpoint_path in enumerate(checkpoint_paths):
    # m = re.match(f'{checkpoint_dir}/checkpoint_(\d+)', checkpoint_path)
    step = int(checkpoint_path.split('_')[-1])
    step_out_list = os.listdir(inference_output)
    step_out_list = [item for item in step_out_list if item.startswith(f'{step}-')]
    if len(step_out_list) == len(texts)*3:
        print(f'step {step} already inferred, continue')
        continue

    model.load_state_dict(torch.load(checkpoint_path)['state_dict'])
    model.eval()

    print(f'[{i_checkpoint}]/[{len(checkpoint_paths)}] infering step {step}')
    for  i_text, text in enumerate(texts):
        # text = "Waveglow is really awesome!"
        sequence = np.array(text_to_sequence(text, ['english_cleaners']))[None, :]
        sequence = torch.autograd.Variable(torch.from_numpy(sequence)).cuda().long()





        mel_outputs, mel_outputs_postnet, _, alignments = model.inference(sequence)
        plot_data((mel_outputs.data.cpu().numpy()[0],
                   mel_outputs_postnet.data.cpu().numpy()[0],
                   alignments.data.cpu().numpy()[0].T),
                  os.path.join(inference_output, f'{step}-{i_text}.png')
                  )





        with torch.no_grad():
            audio = waveglow.infer(mel_outputs_postnet, sigma=0.666)
        wavfile.write(os.path.join(inference_output, f'{step}-{i_text}.wav'), hparams.sampling_rate, audio[0].data.cpu().numpy())




        audio_denoised = denoiser(audio, strength=0.01)[:, 0]
        wavfile.write(os.path.join(inference_output, f'{step}-{i_text}-denoised.wav'), hparams.sampling_rate, audio_denoised[0].cpu().numpy())



