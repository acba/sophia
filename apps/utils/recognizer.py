import os
import sys
import json
import subprocess
import pyaudio

import speech_recognition as sr
from vosk import Model, KaldiRecognizer, SetLogLevel
SetLogLevel(-1)

class Recognizer:
    def stream_to_text(self, stream):
        pass

    def read_file(self, path):
        pass

class VoskRecognizer(Recognizer):

    def __init__(self):

        if not os.path.exists('apps/utils/speechrecognition/model'):
            print("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
            exit(1)

        self.threshold = 0.0
        self.sample_rate = 16000
        self.model = Model('apps/utils/speechrecognition/model')

    def is_valid(self, dado):
        return True if 'text' in dado and dado['text'] != '' else False

    def create_recognizer(self):
        self.recognizer = KaldiRecognizer(self.model, self.sample_rate)

    def cria_el(self, resultado):
        start = resultado['result'][0]['start']
        end   = resultado['result'][len(resultado['result'])-1]['end']
        return {'start': start, 'end': end, 'text': resultado['text']}


    def filter_low_conf(self, dados):
        if 'result' not in dados:
            return dados

        dados_confiaveis = list(filter(lambda x: True if x['conf'] > self.threshold else False, dados['result']))
        text = ''
        for dado in dados_confiaveis:
            text += dado['word'] + ' '
        text = text.strip()

        return {
            'result': dados_confiaveis,
            'text': text
        }

    def stream_to_vtt(self, stream, show=False):
        dados = []
        self.create_recognizer()

        while True:
            data = stream.read(4000)
            if len(data) == 0:
                break
            if self.recognizer.AcceptWaveform(data):
                resultado = json.loads(self.recognizer.Result())
                if show:
                    print('Result')
                    print(resultado)

                resultado = self.filter_low_conf(resultado)
                if self.is_valid(resultado):
                    dados += [self.cria_el(resultado)]

        resultado = json.loads(self.recognizer.FinalResult())
        if show:
            print('FinalResult')
            print(resultado)

        resultado = self.filter_low_conf(resultado)
        if self.is_valid(resultado):
            dados += [self.cria_el(resultado)]

        return dados

    def file_to_vtt(self, path, show=False):
        stream = self.read_file(path)
        return self.stream_to_vtt(stream, show)

    def read_file(self, path):
        params = ['ffmpeg', '-loglevel', 'quiet', '-i', path, '-ar', str(self.sample_rate) , '-ac', '1', '-f', 's16le', '-']
        process = subprocess.Popen(params, stdout=subprocess.PIPE)
        return process.stdout


class SRRecognizer(Recognizer):

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.sample_rate=22050

    def read_file(self, path):
        params = ['ffmpeg', '-loglevel', 'quiet', '-i', path, '-ar', 'str(self.sample_rate)' , '-ac', '1', '-f', 's16le', '-']
        process = subprocess.Popen(params, stdout=subprocess.PIPE)
        return process.stdout

    def to_wav(self, path):
        params = ['ffmpeg', '-loglevel', 'quiet', '-y', '-i', path, '-ar', '22050', f'{path}.wav']
        subprocess.call(params)
        return True

    def file_to_vtt(self, path):
        self.to_wav(path)

        pathwav = path + '.wav'
        texto = ''

        with sr.AudioFile(pathwav) as source:
            audio = self.recognizer.record(source)

            try:
                texto = self.recognizer.recognize_google(audio, language='pt-br')
            except sr.UnknownValueError:
                texto = ''

        return [{
        'start': 0,
        'text': texto
    }]

vr = VoskRecognizer()
gr = SRRecognizer()
