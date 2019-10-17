from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy

from webapp.forms import ArticleForm, CommentInArticleForm
from webapp.models import Article, Comment
from django.views.generic import  ListView, DetailView, CreateView, DeleteView, UpdateView


class IndexView(ListView):
    template_name = 'article/index.html'
    model = Article
    context_object_name = 'articles'
    ordering = ['-created_at']
    paginate_by = 4
    paginate_orphans = 1
    page_kwarg = 'page'


class ArticleView(DetailView):
    template_name = 'article/article.html'
    model = Article
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()
        context['article'] = article
        context['form'] = CommentInArticleForm()
        context['comments'] = Comment.objects.all().filter(article_id=article).order_by('-created_at')
        return context


class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article/create.html'

    def get_success_url(self):
        return reverse('article_view', kwargs={'pk': self.object.pk})


class ArticleUpdateView(UpdateView):
    form_class = ArticleForm
    model = Article
    template_name = 'article/update.html'

    def get_success_url(self):
        return reverse('article_view', kwargs={'pk': self.object.pk})


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'article/delete.html'
    success_url = reverse_lazy('index')
