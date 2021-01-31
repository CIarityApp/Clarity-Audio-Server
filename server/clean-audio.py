import subprocess
import os
import sys
import numpy as np

import wave
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from shutil import copy2 as cp

def get_file_paths():
    """
    Get paths to all audio files.
    """
    audio_folder = os.getcwd() + '/server/assets'

    audio_addy_list = []
    for file in os.scandir(audio_folder):
        audio_addy_list.append(file.path)

    return audio_addy_list

def invert_audio(input, output):
    command = "ffmpeg -i {0} -af aeval=-val(0):c=same {1}".format(input, output)
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

def overlay_audio(voice_addy, bg_addy, final_addy):
    command = "ffmpeg -i {0} -i {1} -filter_complex amix=inputs=2:duration=longest {2}".format(voice_addy, bg_addy, final_addy)
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

def equalize(input, outname):

    dirname= os.getcwd() + '/server/assets'
    wavname = (dirname+'/'+outname+'.wav').replace(" ", "_")
    center = 500
    width = 200
    gain = 30
    # command = 'ffmpeg -i {0} -af lowpass=f=700 {1}'.format(input, wavname)
    command = 'ffmpeg -i {0} -af highpass=f=800,lowpass=f=3000,lowpass=f=3000,lowpass=f=3000,lowpass=f=3000,lowpass=f=3000,lowpass=f=3000,equalizer=f=3000:width_type=h:width=250:g=40,lowpass=f=2500,lowpass=f=2500,lowpass=f=2500 {1}'.format(input, wavname, center, width, gain)
        # EQUALIZER: equalizer=f={2}:width_type=h:width={3}:g={4}
        # BANDREJECT: bandreject=f=12000:width_type=h:width=10000,\x
        # LOWERPASS: lowpass=f=2500 {1}'.format(input, wavname, center, width, gain)
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
 
def create_spectro(infile, outname):
    dirname= os.getcwd() + '/server/assets'
    wavname=(dirname+'/'+outname+'.wav')

    command="ffmpeg -i %s -ar 44100 -ac 1 %s" % (infile, wavname)
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    # Get file info   
    def get_wav_info(wavname):
        wav = wave.open(wavname, 'r')
        frames = wav.readframes(-1)
        sound_info = np.fromstring(frames, 'int16')
        frame_rate = wav.getframerate()
        wav.close()
        return sound_info, frame_rate

    def graph_spectrogram(wavname):
        sound_info, frame_rate = get_wav_info(wavname)
        plt.rcParams['axes.facecolor'] = 'black'
        plt.rcParams['savefig.facecolor'] = 'black'
        plt.rcParams['axes.edgecolor'] = 'white'
        plt.rcParams['lines.color'] = 'white'
        plt.rcParams['text.color'] = 'white'    
        plt.rcParams['xtick.color'] = 'white'    
        plt.rcParams['ytick.color'] = 'white'
        plt.rcParams['axes.labelcolor'] = 'white'
        fig = plt.figure(num=None, figsize=(12, 7.5), dpi=300)
        ax = fig.add_subplot(111)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(30))
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(10))
        ax.yaxis.set_major_locator(ticker.MultipleLocator(1000))
        ax.yaxis.set_minor_locator(ticker.MultipleLocator(500))
        ax.tick_params(axis='both', direction='inout')
        plt.title('Spectrogram')
        plt.xlabel('time in seconds')
        plt.ylabel('Frequency (Khz)')
        plt.specgram(sound_info, Fs=frame_rate, cmap='gnuplot')
        cbar = plt.colorbar()
        cbar.ax.set_ylabel('dB')
        plt.savefig(dirname+'/'+outname+'.png')

    # Save spectrogram
    graph_spectrogram(wavname)

    # Remove wav file and temporary file
    os.remove(wavname)
    # os.remove(music_file_tmp)

def clean_audio(input_addy, bg_addy):
    invert_filename = 'inverted'
    final_filename = 'final'
    invert_addy = os.getcwd() + '/server/assets/tests/' + invert_filename + '.wav'
    final_addy = os.getcwd() + '/server/assets/tests/' + final_filename + '.wav'

    invert_audio(bg_addy, invert_addy)
    overlay_audio(input_addy, invert_addy, final_addy)

    # write the file from final addy to firebase

clean_audio(os.getcwd() + '/server/assets/tests/marc_ambu.mp3', os.getcwd() + '/server/assets/tests/ambu.mp3')