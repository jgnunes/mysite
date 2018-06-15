from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ListaForm, GabaritoForm
from .models import Questao, Resposta

def requerir_lista(request):
   form = ListaForm(request.POST)
   if request.method == "POST":
      if form.is_valid():
          assunto = [str(i) for i in form.cleaned_data.get('assunto', None)]
          disciplina = [str(j) for j in form.cleaned_data.get('disciplina', None)]
          max_questoes = form.cleaned_data.get('max_questoes', None)
          request.session['requerir'] = request.POST.get('requerir', [assunto, disciplina, max_questoes])
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
    respostas_gabarito = []
    assunto = request.session.get('requerir')[0]
    disciplina = request.session.get('requerir')[1]
    max_questoes = request.session.get('requerir')[2]

    form = GabaritoForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            if not assunto:
                questoes_queryset = Questao.objects.filter(disciplinas__nome__in=disciplina)[:max_questoes]
            else:
                questoes_queryset = Questao.objects.filter(tags__assunto__in=assunto, disciplinas__nome__in=disciplina)[:max_questoes]
            for questao in questoes_queryset:
                resposta_correta = Resposta.objects.filter(questao_id=questao.id)[5]
                respostas_gabarito.append(str(resposta_correta).replace("'", ''))
            request.session['criar'] = request.POST.get('criar', respostas_gabarito)
            # redirect to the url where you'll process the input
            return redirect('listas:gabarito')  # insert reverse or url

    #se nenhum assunto tiver sido selecionado, apenas disciplina(s)
    #assunto nao sera usado para filtrar as questoes
    if not assunto:
        questoes_queryset = Questao.objects.filter(disciplinas__nome__in=disciplina)[:max_questoes]
        for questao in questoes_queryset:
            respostas_queryset = Resposta.objects.filter(questao_id=questao.id)[:5]
            for resposta in respostas_queryset:
                respostas.append(str(resposta).replace('<p>', '').replace('</p>', '').replace("'", ""))
            questao = str(questao).replace('<p>', '').replace("'", "")
            questao = tuple(questao.split("</p>")[:-1])
            questoes[questao] = respostas
            respostas = []
        return render(request, 'listas/lista_criada.html', {'questoes': questoes})

    else:
        questoes_queryset = Questao.objects.filter(tags__assunto__in=assunto, disciplinas__nome__in=disciplina)[:max_questoes]
        for questao in questoes_queryset:
            respostas_queryset = Resposta.objects.filter(questao_id=questao.id)[:5]
            for resposta in respostas_queryset:
                respostas.append(str(resposta).replace('<p>', '').replace('</p>', '').replace("'", ""))
            questao = str(questao).replace('<p>', '').replace("'", "")
            questao = tuple(questao.split('</p>')[:-1])
            print("questao:", questao)
            questoes[questao] = respostas
            respostas = []

        return render(request, 'listas/lista_criada.html', {'questoes': questoes})

def criar_gabarito(request):
    respostas = request.session.get('criar')
    print(respostas)
    return render(request, 'listas/gabarito.html', {'respostas': respostas})