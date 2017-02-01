#!/usr/bin/env python

import argparse
import ConfigParser as configparser
import json
import hashlib
from os.path import join, dirname, exists
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
    parser.add_argument('text', nargs=1)
    args = parser.parse_args()
    return args


def generate_speech(text):
    fname = hashlib.sha256(text).hexdigest() + ".wav"
    fullfile = join(dirname(__file__), "audio", fname)
    if not exists(fullfile):
        user, passwd = get_config()
        tts = TextToSpeechV1(
            username=user,
            password=passwd,
            x_watson_learning_opt_out=True)
        with open(fullfile, 'wb') as f:
            f.write(tts.synthesize(text, accept='audio/wav', voice="en-US_AllisonVoice"))
    print(fullfile)


def main():
    args = parse_args()
    generate_speech(args.text[0])


if __name__ == "__main__":
    main()
