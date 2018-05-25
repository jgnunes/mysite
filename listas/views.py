from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ListaForm
from .models import Questao, Resposta


def requerir_lista(request):
   form = ListaForm(request.POST)
   if request.method == "POST":
      if form.is_valid():
          assunto = str(form.cleaned_data.get('opcoes', None))
          request.session['requerir'] = request.POST.get('requerir', assunto)
         #redirect to the url where you'll process the input
          return redirect('listas:criar') # insert reverse or url
   errors = form.errors or None # form not submitted or it has errors
   return render(request, 'users/dashboard.html',{
          'form': form,
          'errors': errors,
   })

def criar_lista(request):
    questoes = {}
    respostas = []
    assunto = request.session.get('requerir')
    questoes_queryset = Questao.objects.filter(tags__assunto=assunto)
    for questao in questoes_queryset:
        respostas_queryset = Resposta.objects.filter(questao_id=questao.id)
        for resposta in respostas_queryset:
            respostas.append(str(resposta))
        # respostas.append(str(Resposta.objects.filter(questao_id=questao.id)))
        questao = str(questao)
        questoes[questao] = respostas
        respostas = []

    return render(request, 'listas/lista_criada.html', {'questoes': questoes})