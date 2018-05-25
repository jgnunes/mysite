from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Lista(models.Model):
    user = models.ForeignKey(User, related_name='lista', on_delete = models.CASCADE, blank=True, null=True)
    generated_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return '{}: {}'.format(self.generated_at, self.user)

class Questao(models.Model):
    lista = models.ForeignKey(Lista, related_name='listas', on_delete = models.CASCADE, blank=True, null=True)
    texto = models.CharField(max_length=500, default="")
    # tags = models.CharField(max_length=500, default="")
    data_de_upload = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.texto

class Resposta(models.Model):
    questao = models.ForeignKey(Questao, on_delete = models.CASCADE, related_name='respostas', default="", blank=True, null=True)
    texto = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.texto

class Tag(models.Model):
    questao = models.ManyToManyField(Questao, related_name='tags', default="", blank=True)
    assunto = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.assunto



