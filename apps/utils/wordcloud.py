import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

from io import BytesIO
import base64

from .textprocessor import NLTK_PT, STOPWORDS_EXTRA

class WordCloud:

    def __init__(self):
        pass

    def generate_wordcloud(texto):

        # lista de stopwords
        stopwords = set(STOPWORDS)
        stopwords.update(NLTK_PT)
        stopwords.update(STOPWORDS_EXTRA)

        wc = WordCloud(stopwords=stopwords, background_color="white", width=1600, height=800, collocations=False)
        wc.generate(texto)

        return wc

    def wc2base64(wc):
        plt.axis("off")
        plt.imshow(wc, interpolation="bilinear")

        arquivo = BytesIO()
        plt.savefig(arquivo, format='png', dpi=1200)
        arquivo.seek(0)
        return base64.b64encode(arquivo.getvalue()).decode('utf-8')
