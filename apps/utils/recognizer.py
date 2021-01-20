import os
import sys
import json
import subprocess
import pyaudio

import speech_recognition as sr
from vosk import Model, KaldiRecognizer, SetLogLevel

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
        self.recognizer = KaldiRecognizer(self.model, self.sample_rate)

    def is_valid(self, dado):
        return True if 'text' in dado and dado['text'] != '' else False


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

    def stream_to_text(self, stream):
        dados = self.stream_to_vtt(self.recognizer, stream)
        texto = ''
        for d in dados:
            texto += d['text'] + ' '

        return texto.strip()

    def stream_to_vtt(self, stream):
        dados = []

        while True:
            data = stream.read(4000)
            if len(data) == 0:
                break
            if self.recognizer.AcceptWaveform(data):
                resultado = json.loads(self.recognizer.Result())
                resultado = self.filter_low_conf(resultado)
                if self.is_valid(resultado):
                    dados += [self.cria_el(resultado)]

        resultado = json.loads(self.recognizer.FinalResult())
        resultado = self.filter_low_conf(resultado)
        if self.is_valid(resultado):
            dados += [self.cria_el(resultado)]

        return dados

    def file_to_vtt(self, path):
        stream = self.read_file(path)
        return self.stream_to_vtt(stream)

    def mic_to_text(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
        stream.start_stream()

        texto_transcrito = []
        while True:
            data = stream.read(4000)
            if len(data) == 0:
                break
            if self.recognizer.AcceptWaveform(data):
                resultado = self.recognizer.Result()
                parcial = json.loads(resultado)['text']

                if parcial != '':
                    texto_transcrito.append(parcial)

                if parcial == 'fechar' or parcial == 'fim':
                    break

        resultado = self.recognizer.FinalResult()
        texto_transcrito.append(json.loads(resultado)['text'])

        return texto_transcrito

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
