import pdfplumber
import re
import nltk
import textract
import datetime
from webvtt import WebVTT, Caption
import time

from docx import Document

from validate_docbr import CPF, CNPJ


def init_nltk():
    nltk.download('rslp')
    nltk.download('stopwords')
    nltk.download('omw')

def get_nltk_pt():
    stopwords = None
    try:
        stopwords = nltk.corpus.stopwords.words('portuguese')
    except LookupError:
        init_nltk()
        stopwords = nltk.corpus.stopwords.words('portuguese')

    return stopwords

STOPWORDS_EXTRA = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
    'u', 'v', 'x', 'w', 'y', 'z', 'de', 'da', 'das',
    'do', 'dos', '-', '–'
]

def formata_dado(dado, mask):
    if len(dado) != len(re.sub(r'[^#]', '', mask)):
        return dado

    _mask = mask.replace('#', '{}')
    return _mask.format(*f'{dado}')

def convert_ts(dado):
    inicial = time.strftime('%H:%M:%S', time.gmtime(dado))
    milisegundos = '000' if str(dado%1) == '0' else str(10.58%1).split('.')[1][:3]

    return f'{inicial}.{milisegundos}'

def write_vtt(lista_dict, path):
    # start, end, text
    vtt = WebVTT()

    with open(path, 'w') as writer:
        for dado in lista_dict:
            caption = Caption(
                convert_ts(dado['start']),
                convert_ts(dado['end']),
                dado['text']
            )
            vtt.captions.append(caption)
        vtt.write(writer)




def tp_factory(data, mime):

    if mime == 'application/pdf':
        return PDFProcessor(data)
    elif mime == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        return DOCXProcessor(data)
    elif mime == 'text/plain':
        return TXTProcessor(data)
    else:
        return GenericProcessor(data)


class TextProcessor:
    def __init__(self, data):
        if type(data) == str:
            self.text = data
        else:
            self.file = data

    def filter_cpf(self):
        regra  = '([0-9]{3}[\.]?[0-9]{3}[\.]?[0-9]{3}[-]?[0-9]{2})'
        encontrados = re.findall(regra, self.text)
        encontrados = list(map(lambda x: re.sub(r'\D', '', x), encontrados))

        test = CPF()
        encontrados = list(filter(lambda x: test.validate(x), encontrados))
        encontrados = list(map(lambda x: formata_dado(x, '###.###.###-##'), encontrados))

        return encontrados

    def filter_cnpj(self):
        regra = '([0-9]{2}\.?[0-9]{3}\.?[0-9]{3}\/?[0-9]{4}\-?[0-9]{2})'
        encontrados = re.findall(regra, self.text)
        encontrados = list(map(lambda x: re.sub(r'\D', '', x), encontrados))

        test = CNPJ()
        encontrados = list(filter(lambda x: test.validate(x), encontrados))
        encontrados = list(map(lambda x: formata_dado(x, '##.###.###/####-##'), encontrados))

        return encontrados

    def filter_email(self):
        regra = '([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)'
        encontrados = re.findall(regra, self.text)
        return encontrados

    def filter_telefone(self):
        regra = '(\(?\d{2}\)?\s?\d{4,5}\-\d{4})'
        encontrados = re.findall(regra, self.text)
        return encontrados

    def filter_urls(self):
        regra = '(https?:\/\/)?(www\.)[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,4}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)|(https?:\/\/)?(www\.)?(?!ww)[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,4}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'
        encontrados = re.findall(regra, self.text)
        return encontrados

    def info(self):
        cpfs      = self.filter_cpf()
        cnpjs     = self.filter_cnpj()
        emails    = self.filter_email()
        telefones = self.filter_telefone()
        urls      = self.filter_urls()

        tokens = self.remove_stopwords().split(' ')
        mais_frequentes = nltk.FreqDist(tokens).most_common(20)

        return { 'cpfs': cpfs, 'cnpjs': cnpjs, 'emails': emails, 'telefones': telefones, 'urls': urls, 'mais_frequentes': mais_frequentes}

    def remove_stopwords(self, _set=False):
        # tratado = [token.lower() for token in self.text.split() if token not in get_nltk_pt() and token not in STOPWORDS_EXTRA]
        tratado = []
        for token in self.text.split():
            token = token.lower()
            if token not in get_nltk_pt() and token not in STOPWORDS_EXTRA:
                tratado.append(token)

        if _set:
            self.text = ' '.join(tratado)
        return ' '.join(tratado)

    def clean(self):
        self.text = self.text.replace('\n', ' ').replace('\t', ' ')
        return self.text

class PDFProcessor(TextProcessor):
    def extract(self):
        texto_completo = ''
        path = self.file.path if hasattr(self, 'file') else self.text

        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                pg_texto = page.extract_text()
                pg_num   = page.page_number
                texto_completo += ' ' + pg_texto

        self.text = texto_completo.strip()
        return self.text

class DOCXProcessor(TextProcessor):
    def extract(self):
        texto_completo = ''
        path = self.file.path if hasattr(self, 'file') else self.text

        document = Document(path)

        for p in document.paragraphs:
            texto_completo += ' ' + p.text

        self.text = texto_completo.strip()
        return self.text

class TXTProcessor(TextProcessor):
    def extract(self):
        path = self.file.path if hasattr(self, 'file') else self.text

        reader = open(path)
        linhas = reader.readlines()
        texto_completo = ' '.join(linhas)

        self.text = texto_completo.strip()
        return self.text

class GenericProcessor(TextProcessor):
    def extract(self):
        path = self.file.path if hasattr(self, 'file') else self.text

        text = textract.process(path)
        self.text = text.decode('utf-8')

        return self.text

