import pdfplumber
import re
import nltk
from nltk.tokenize import RegexpTokenizer

NLTK_PT = nltk.corpus.stopwords.words('portuguese')
STOPWORDS_EXTRA = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
    'u', 'v', 'x', 'w', 'y', 'z'
]

def init_nltk():
    nltk.download('rslp')
    nltk.download('stopwords')
    nltk.download('omw')

init_nltk()

class TextProcessor:
    def __init__(self, file):
        self.file = file

        if self.get_filetype() == 'application/pdf':
            return PDFProcessor(self.file)

    def get_filetype(self):
        return 'application/pdf'

    # def extract(self, path):
    #     if self.get_filetype(path) == 'application/pdf':
    #         return extract_pdf(path)
    #     else:
    #         print('Formato nao suportado')

    def filter_cpf(self):
        regra  = '([0-9]{3}[\.]?[0-9]{3}[\.]?[0-9]{3}[-]?[0-9]{2})'
        encontrados = re.findall(regra, self.text)
        return encontrados

    def filter_cnpj(self):
        regra = '([0-9]{2}\.?[0-9]{3}\.?[0-9]{3}\/?[0-9]{4}\-?[0-9]{2})'
        encontrados = re.findall(regra, self.text)
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

class PDFProcessor(TextProcessor):
    def __init__(self, file):
        self.file = file

    def extract(self):
        texto_completo = ''
        with pdfplumber.open(self.file.path) as pdf:
            for page in pdf.pages:
                pg_texto = page.extract_text()
                pg_num = page.page_number
                texto_completo+= ' ' + pg_texto

        self.text = texto_completo
        return texto_completo

    def clean(self):
        self.text = self.text.replace('\n', ' ')
        return self.text

    def remove_stopwords(self, set=False):
        tratado = [token.lower() for token in self.text.split() if token not in NLTK_PT and token not in STOPWORDS_EXTRA]
        if set:
            self.text = ' '.join(tratado)
        return ' '.join(tratado)

    def info(self):
        cpfs      = self.filter_cpf()
        cnpjs     = self.filter_cnpj()
        emails    = self.filter_email()
        telefones = self.filter_telefone()
        urls      = self.filter_urls()

        texto_tratado = self.remove_stopwords()
        mais_frequentes = nltk.FreqDist(texto_tratado).most_common(20)

        return { 'cpfs': cpfs, 'cnpjs': cnpjs, 'emails': emails, 'telefones': telefones, 'urls': urls, 'mais_frequentes': mais_frequentes}
