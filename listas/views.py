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
          assunto = [str(i) for i in form.cleaned_data.get('assunto', None)]
          disciplina = [str(j) for j in form.cleaned_data.get('disciplina', None)]
          request.session['requerir'] = request.POST.get('requerir', [assunto, disciplina])
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
    assunto = request.session.get('requerir')[0]
    disciplina = request.session.get('requerir')[1]
    print("assunto", assunto)
    print("disciplina", disciplina)

    #se nenhum assunto tiver sido selecionado, apenas disciplina(s)
    #assunto nao sera usado para filtrar as questoes
    if not assunto:
        questoes_queryset = Questao.objects.filter(disciplinas__nome__in=disciplina)
        for questao in questoes_queryset:
            respostas_queryset = Resposta.objects.filter(questao_id=questao.id)
            for resposta in respostas_queryset:
                respostas.append(str(resposta).replace('<p>', '').replace('</p>', '').replace("'", ""))
            questao = str(questao).replace('<p>', '').replace("'", "")
            questao = tuple(questao.split('</p>'))
            questoes[questao] = respostas
            respostas = []

        return render(request, 'listas/lista_criada.html', {'questoes': questoes})

    else:
        questoes_queryset = Questao.objects.filter(tags__assunto__in=assunto, disciplinas__nome__in=disciplina)
        for questao in questoes_queryset:
            respostas_queryset = Resposta.objects.filter(questao_id=questao.id)
            for resposta in respostas_queryset:
                respostas.append(str(resposta).replace('<p>', '').replace('</p>', '').replace("'", ""))
            questao = str(questao).replace('<p>', '').replace("'", "")
            questao = tuple(questao.split('</p>'))
            questoes[questao] = respostas
            respostas = []

        return render(request, 'listas/lista_criada.html', {'questoes': questoes})