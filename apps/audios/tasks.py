import traceback
from django.core.files import File
from celery import shared_task
from celery.utils.log import get_task_logger
from celery_progress.backend import ProgressRecorder

from apps.audios.models import AudioDocument, ProcessedAudio, TermoFreqData, LegendaTrecho

from apps.utils import silent_remove
from apps.utils.wordcloud import WordCloudProcessor
from apps.utils.textprocessor import TextProcessor, write_vtt
from apps.utils.recognizer import vr, gr

from config import celery_app

logger = get_task_logger(__name__)

# @celery_app.task(name='processa_textdoc_task')
@shared_task(bind=True)
def processa_audiodoc_task(self, processor, userid, audioid):
    '''
        Tarefa para processar algum audio.
    '''

    progress_recorder = ProgressRecorder(self)
    audiodoc = AudioDocument.objects.filter(user__id=userid, id=audioid).first()
    progress_recorder.set_progress(1, 6, description='Processando')

    if audiodoc.foi_processado:
        return {'status': False}

    try:
        if processor == 'vr':
            proc = 'Vosk'
            lista_vtt = vr.file_to_vtt(audiodoc.file.path)
        elif processor == 'gr':
            proc = 'Google'
            lista_vtt = gr.file_to_vtt(audiodoc.file.path)
        # Default é o VOSK
        else:
            proc = 'Vosk'
            lista_vtt = vr.file_to_vtt(audiodoc.file.path)

        progress_recorder.set_progress(2, 6, description='Processando')

        texto = ''
        for t in lista_vtt:
            texto += t['text'] + ' '
        texto = texto.strip()

        tp = TextProcessor(texto)
        tp.clean()
        info = tp.info()
        progress_recorder.set_progress(3, 6, description='Processando')

        # Cria ProcessedAudio
        pa = ProcessedAudio.objects.create(audiodoc=audiodoc, processor=proc)

        # Cria LegendaFile
        write_vtt(lista_vtt, f'{audiodoc.file.path}.vtt')
        django_file = File(open(f'{audiodoc.file.path}.vtt','rb'))
        pa.file_legenda.save(f'{audiodoc.filename}.vtt', django_file)
        pa.save()

        # Exclui arquivo temporario criado
        silent_remove(f'{audiodoc.file.path}.vtt')

        # Cria o arquivo Wordcloud
        wp = WordCloudProcessor(tp.remove_stopwords())
        wp.generate_wordcloud()
        wp.wc2png(audiodoc.file.path)
        django_file = File(open(f'{audiodoc.file.path}.wordcloud.png','rb'))
        pa.file_wc.save(f'{audiodoc.filename}.wordcloud.png', django_file)
        pa.save()
        progress_recorder.set_progress(4, 6, description='Processando')

        # Exclui arquito temporario criado
        silent_remove(f'{audiodoc.file.path}.wordcloud.png')

        # Cria Trechos de Legenda
        for trecho in lista_vtt:
            l = LegendaTrecho(start=trecho['start'], text=trecho['text'], pdoc=pa)
            l.save()
        progress_recorder.set_progress(5, 6, description='Processando')

        # Cria Informacoes de dados mais frequentes
        for dado in info['mais_frequentes']:
            c = TermoFreqData.objects.create(termo=dado[0], qtd=dado[1], pdoc=pa)
            c.save()
        progress_recorder.set_progress(6, 6, description='Processando')

        audiodoc.processando    = False
        audiodoc.foi_processado = True
        audiodoc.save()

        return {'status': True}
    except Exception:
        print(traceback.print_exc())

        audiodoc.processando    = False
        audiodoc.foi_processado = False
        audiodoc.save()

        return {'status': False}

