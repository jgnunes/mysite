from django import forms

from . import models
from . models import Tag, Disciplina

class ListaForm(forms.Form):
    disciplinas_objects = Disciplina.objects.all().order_by('nome')
    disciplina = forms.ModelMultipleChoiceField(queryset=disciplinas_objects)

    assuntos_objects = Tag.objects.all().order_by('assunto')
    assunto = forms.ModelMultipleChoiceField(queryset=assuntos_objects, required=False)

    selecionar_tudo = forms.BooleanField(required=False)

class GabaritoForm(forms.Form):
    pass


# class ListaForm(forms.ModelForm):
#     class Meta:
#         fields = ('assunto',)
#         model = models.Tag