from django.utils.html import format_html
import django_tables2 as tables
from django_tables2.utils import A

from apps.utils import sizeof_fmt
from .models import AudioDocument

class AudioDocumentTable(tables.Table):
    class Meta:
        template_name = 'django_tables2/bootstrap4.html'

    nome           = tables.Column(verbose_name='Descrição', linkify={
        "viewname": "audios:audio",
        "args": [tables.A("pk")]
    })
    filename       = tables.Column(verbose_name='Arquivo')
    size           = tables.Column(verbose_name='Tamanho')
    conteudo       = tables.Column(accessor='file', verbose_name='Conteúdo')
    foi_processado = tables.BooleanColumn(verbose_name='Transcrito')
    processor      = tables.Column(accessor='processedaudio__processor')
    preview        = tables.Column(accessor='processedaudio', verbose_name='Preview')
    remover        = tables.Column(accessor='nome', verbose_name='Remover', linkify={
        "viewname": "audios:remove_audio",
        "args": [tables.A("pk")]
    })

    def render_nome(self, value, record):
        return format_html(f'<span style="color: #007bff;" class="hvr-grow">{record.nome}</span>')

    def render_size(self, value, record):
        return format_html(f'{sizeof_fmt(value)}')

    def render_conteudo(self, value, record):
        return format_html(f'<audio src="{value.url}" controls></audio>')

    def render_preview(self, value, record):
        return format_html(f'<span class="font-italic">{value}</span>')

    def render_remover(self, value, record):
        return format_html(f'<i style="color: #007bff;" class="fa fa-times hvr-grow" aria-hidden="true"></i>')
