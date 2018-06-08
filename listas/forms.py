from django import forms

from . import models
from . models import Tag, Disciplina

class ListaForm(forms.Form):
    disciplinas_objects = Disciplina.objects.all().order_by('nome')
    disciplina = forms.ModelMultipleChoiceField(queryset=disciplinas_objects)

    assuntos_objects = Tag.objects.all().order_by('assunto')
    assunto = forms.ModelMultipleChoiceField(queryset=assuntos_objects, required=False)

    def get_assunto(self):
        ''' returns the name of the selected language '''
        try:
            return str(self.assuntos.get(assunto='biologia celular'))
        except:
            return 10

# class ListaForm(forms.ModelForm):
#     class Meta:
#         fields = ('assunto',)
#         model = models.Tag