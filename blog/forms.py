from django import forms

from . import models
from . models import Post, Autor

class PublicationForm(forms.Form):
    posts_objects = Post.objects.all().order_by('titulo')
    post = forms.ModelChoiceField(queryset=posts_objects)
