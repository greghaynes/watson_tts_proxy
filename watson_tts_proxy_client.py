#!/usr/bin/env python

import argparse
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
import json
import hashlib
from os.path import join, dirname, exists

import pyaudio
import wave
from watson_developer_cloud import TextToSpeechV1


def get_config():
    config = configparser.RawConfigParser()
    config.read('speech.cfg')
    user = config.get('auth', 'username')
    password = config.get('auth', 'password')
    return (user, password)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Create speech content from text')
    parser.add_argument('-p', '--proxy',
                        default='http://localhost:8888',
                        help="Proxy host to use for Watson TTS")
    parser.add_argument('text', nargs=1)
    args = parser.parse_args()
    return args


def generate_speech(text, proxy):
    fullfile = join(dirname(__file__), "proxy.wav")
    user, passwd = get_config()
    tts = TextToSpeechV1(
        url=proxy,
        username=user,
        password=passwd,
        x_watson_learning_opt_out=True)
    with open(fullfile, 'wb') as f:
        f.write(tts.synthesize(text, accept='audio/wav',
                               voice="en-US_AllisonVoice"))
    play_file(fullfile)
    print(fullfile)


def play_file(fname):
    # create an audio object
    wf = wave.open(fname, 'rb')
    p = pyaudio.PyAudio()
    chunk = 1024

    # open stream based on the wave object which has been input.
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # read data (based on the chunk size)
    data = wf.readframes(chunk)

    # play stream (looping from beginning of file to the end)
    while data != b'':
        # writing to the stream is what *actually* plays the sound.
        stream.write(data)
        data = wf.readframes(chunk)

        # cleanup stuff.
    stream.close()
    p.terminate()


def main():
    args = parse_args()
    generate_speech(args.text[0], args.proxy)


if __name__ == "__main__":
    main()
