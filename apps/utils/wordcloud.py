import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

from io import BytesIO
import base64

from .textprocessor import get_nltk_pt, STOPWORDS_EXTRA

class WordCloudProcessor:

    def __init__(self, texto):
        self.texto = texto

    def generate_wordcloud(self):

        # lista de stopwords
        stopwords = set(STOPWORDS)
        stopwords.update(get_nltk_pt())
        stopwords.update(STOPWORDS_EXTRA)

        self.wc = WordCloud(stopwords=stopwords, background_color='white', width=1600, height=800, collocations=False)
        self.wc.generate(self.texto)

        return self.wc

    def wc2base64(self):
        plt.axis('off')
        plt.imshow(self.wc, interpolation='bilinear')

        arquivo = BytesIO()
        plt.savefig(arquivo, format='png', dpi=1200)
        arquivo.seek(0)
        return base64.b64encode(arquivo.getvalue()).decode('utf-8')


    def wc2png(self, path):
        plt.axis('off')
        plt.imshow(self.wc, interpolation='bilinear')
        plt.savefig(f'{path}.wordcloud.png', format='png', dpi=1200, bbox_inches='tight')

    # def wc2svg(self, path):
    #     plt.axis('off')
    #     plt.imshow(self.wc, interpolation='bilinear')

    #     # arquivo = BytesIO()
    #     plt.imshow(self.wc, interpolation="bilinear")
    #     plt.savefig(f'{path}.wordcloud.svg', format='svg')
    #     # arquivo.seek(0)
    #     # return str(arquivo.getvalue())

