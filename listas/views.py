from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ListaForm, GabaritoForm
from .models import Questao, Resposta
from itertools import chain

def filtrar_questoes(palavra_chave, assunto, disciplina, max_questoes):
    #se o campo palavra chave nao estiver vazio
    if palavra_chave != ['']:
        questoes_queryset = Questao.objects.filter(tags__assunto__in = palavra_chave)[:max_questoes]

    #se os campos assunto e disciplina nao estiverem vazios
    elif assunto != [] and disciplina != []:
        # questoes_queryset = Questao.objects.filter(tags__assunto__in=assunto,
        #                                            disciplinas__nome__in=disciplina)[:max_questoes]
        questoes_queryset1 = Questao.objects.filter(tags__assunto__in=assunto)
        questoes_queryset2 = Questao.objects.filter(disciplinas__nome__in=disciplina)

        #se o usuario nao der um numero maximo de questoes, os querysets nao sao cortados
        if not max_questoes:
            max_questoes_assunto = max_questoes
            max_questoes_disciplina = max_questoes
        else:
            #se o numero de questoes filtradas por assunto for menor que a metade do numero maximo
            #de questoes, entao as questoes obtidas pelo filtro de disciplina irao completar ate
            #que seja alcancado o numero maximo de questoes dado pelo usuario
            if len(questoes_queryset1) < max_questoes/2:
                toComplete = max_questoes/2 - len(questoes_queryset1)
                max_questoes_disciplina = max_questoes/2 + toComplete
                max_questoes_assunto = max_questoes/2

            #mesmo racional do if acima, mas nesse caso, o numero de questoes filtradas por disciplina
            #eh o que nao eh suficiente para completar metade das questoes pedidas pelo usuario
            if len(questoes_queryset2) < max_questoes/2:
                toComplete = max_questoes/2 - len(questoes_queryset2)
                max_questoes_assunto = max_questoes/2 + toComplete
                max_questoes_disciplina = max_questoes/2

            else:
                max_questoes_assunto = max_questoes/2
                max_questoes_disciplina = max_questoes - max_questoes_assunto

        # first filter by assunto and then, by disciplina
        questoes_queryset1 = Questao.objects.filter(tags__assunto__in=assunto)[:max_questoes_assunto]
        questoes_queryset2 = Questao.objects.filter(disciplinas__nome__in=disciplina)[:max_questoes_disciplina]
        # merge queryset1 and quesyset2
        questoes_queryset = chain(questoes_queryset1, questoes_queryset2)

    elif assunto != []:
        questoes_queryset = Questao.objects.filter(tags__assunto__in=assunto)[:max_questoes]

    elif disciplina != []:
        questoes_queryset = Questao.objects.filter(disciplinas__nome__in = disciplina)[:max_questoes]

    return questoes_queryset

def requerir_lista(request):
   form = ListaForm(request.POST)
   if request.method == "POST":
      if form.is_valid():
          assunto = [str(i) for i in form.cleaned_data.get('assunto', None)]
          disciplina = [str(j) for j in form.cleaned_data.get('disciplina', None)]
          palavra_chave = [form.cleaned_data.get('palavra_chave', None)]
          max_questoes = form.cleaned_data.get('max_questoes', None)
          request.session['requerir'] = request.POST.get('requerir', [assunto, disciplina, palavra_chave, max_questoes])
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
    palavra_chave = request.session.get('requerir')[2]
    max_questoes = request.session.get('requerir')[3]

    form = GabaritoForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            questoes_queryset = filtrar_questoes(palavra_chave, assunto, disciplina, max_questoes)
            for questao in questoes_queryset:
                resposta_correta = Resposta.objects.filter(questao_id=questao.id)[5]
                respostas_gabarito.append(str(resposta_correta).replace("'", ''))
            request.session['criar'] = request.POST.get('criar', respostas_gabarito)
            # redirect to the url where you'll process the input
            return redirect('listas:gabarito')  # insert reverse or url

    questoes_queryset = filtrar_questoes(palavra_chave, assunto, disciplina, max_questoes)
    for questao in questoes_queryset:
        respostas_queryset = Resposta.objects.filter(questao_id=questao.id)[:5]
        for resposta in respostas_queryset:
            respostas.append(str(resposta).replace('<p>', '').replace('</p>', '').replace("'", ""))
        questao = str(questao).replace('<p>', '').replace("'", "")
        questao = tuple(questao.split("</p>")[:-1])
        questoes[questao] = respostas
        respostas = []
    return render(request, 'listas/lista_criada.html', {'questoes': questoes})

def criar_gabarito(request):
    respostas = request.session.get('criar')
    print(respostas)
    return render(request, 'listas/gabarito.html', {'respostas': respostas})