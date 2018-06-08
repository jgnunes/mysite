from django.core.management.base import BaseCommand
from listas.models import Tag, Resposta, Questao, Disciplina

class Command(BaseCommand):

    def _delete_questions(self):
        Questao.objects.all().delete()

    def _delete_answers(self):
        Resposta.objects.all().delete()

    def _delete_tags(self):
        Tag.objects.all().delete()

    def _delete_disciplinas(self):
        Disciplina.objects.all().delete()

    def handle(self, *args, **options):
        self._delete_questions()
        self._delete_answers()
        self._delete_tags()
        self._delete_disciplinas()