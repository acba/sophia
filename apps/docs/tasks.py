from django.core.files import File
from celery import shared_task
from celery.utils.log import get_task_logger
from celery_progress.backend import ProgressRecorder

from apps.utils.textprocessor import tp_factory
from apps.utils.wordcloud import WordCloudProcessor
from apps.utils import silent_remove
from apps.docs.models import TextDocument, ProcessedText, CPFData, CNPJData, EmailData, URLData, TelefoneData, TermoFreqData

from config import celery_app

logger = get_task_logger(__name__)

# @celery_app.task(name='processa_textdoc_task')
@shared_task(bind=True)
def processa_textdoc_task(self, userid, docid):
    '''
        Tarefa para processar algum documento.
    '''

    progress_recorder = ProgressRecorder(self)
    textdoc = TextDocument.objects.filter(user__id=userid, id=docid).first()

    tp = tp_factory(textdoc.file, textdoc.mime)
    texto = tp.extract()
    texto = tp.clean()
    info  = tp.info()
    progress_recorder.set_progress(1, 8, description='Processando')


    # Cria ProcessedText
    pt = ProcessedText.objects.create(texto=texto, textdoc=textdoc)

    # Cria o arquivo WordCloud
    wp = WordCloudProcessor(tp.remove_stopwords())
    wp.generate_wordcloud()
    wp.wc2png(textdoc.file.path)
    django_file = File(open(f'{textdoc.file.path}.wordcloud.png','rb'))
    pt.file_wc.save(f'{textdoc.filename}.wordcloud.png', django_file)
    pt.save()
    progress_recorder.set_progress(2, 8, description='Processando')

    # Exclui arquito temporario criado
    silent_remove(f'{textdoc.file.path}.wordcloud.png')

    # Salva os dados encontrados no texto processado
    for cpf in info['cpfs']:
        c = CPFData.objects.create(cpf=cpf, pdoc=pt)
        c.save()
    progress_recorder.set_progress(3, 8, description='Processando')

    for cnpj in info['cnpjs']:
        c = CNPJData.objects.create(cnpj=cnpj, pdoc=pt)
        c.save()
    progress_recorder.set_progress(4, 8, description='Processando')

    for email in info['emails']:
        c = EmailData.objects.create(email=email, pdoc=pt)
        c.save()
    progress_recorder.set_progress(5, 8, description='Processando')

    for url in info['urls']:
        c = URLData.objects.create(url=url, pdoc=pt)
        c.save()
    progress_recorder.set_progress(6, 8, description='Processando')

    for telefone in info['telefones']:
        c = TelefoneData.objects.create(telefone=telefone, pdoc=pt)
        c.save()
    progress_recorder.set_progress(7, 8, description='Processando')

    # Cria Informacoes de dados mais frequentes
    for dado in info['mais_frequentes']:
        c = TermoFreqData.objects.create(termo=dado[0], qtd=dado[1], pdoc=pt)
        c.save()
    progress_recorder.set_progress(8, 8, description='Processando')

    textdoc.processando    = False
    textdoc.foi_processado = True
    textdoc.save()

    return {'status': True}
