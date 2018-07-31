from django.shortcuts import render, redirect, render_to_response
from blog.models import Post
from django.http import HttpResponseRedirect
# from django.views.generic import TemplateView

def home_page(request):
    posts = []
    posts_objects = Post.objects.all().order_by('data')[::-1][:3] #pegar os 3 posts mais recentes
    for post in posts_objects:
        posts.append([post.titulo, post.texto.split('\n')[0], post.imagem])
    return render(request, 'index.html', {'posts': posts})