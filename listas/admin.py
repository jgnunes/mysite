from django.contrib import admin

from . import models

# admin.site.register(models.Lista)
admin.site.register(models.Questao)
admin.site.register(models.Resposta)
admin.site.register(models.Tag)