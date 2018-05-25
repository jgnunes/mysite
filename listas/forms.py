from django import forms

from . import models
from . models import Tag

class ListaForm(forms.Form):
    assuntos = Tag.objects.all().order_by('assunto')
    opcoes = forms.ModelChoiceField(queryset=assuntos)

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