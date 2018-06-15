from django import forms

from . import models
from . models import Tag, Disciplina

class ListaForm(forms.Form):
    disciplinas_objects = Disciplina.objects.all().order_by('nome')
    disciplina = forms.ModelMultipleChoiceField(queryset=disciplinas_objects,
                                                help_text="Para selecionar mais de uma disciplina, segure a tecla Ctrl e clique sobre as disciplinas de interesse")

    assuntos_objects = Tag.objects.all().order_by('assunto')
    assunto = forms.ModelMultipleChoiceField(queryset=assuntos_objects, required=False)

    max_questoes = forms.IntegerField(label=u"Limite de questões",
                                      help_text= u"Qual o máximo de questões que você deseja?",
                                      min_value=1)

    # selecionar_tudo = forms.BooleanField(required=False)

class GabaritoForm(forms.Form):
    pass


# class ListaForm(forms.ModelForm):
#     class Meta:
#         fields = ('assunto',)
#         model = models.Tag