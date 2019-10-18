from django.db.models import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from webapp.forms import ArticleForm, CommentInArticleForm, SimpleSearchForm
from webapp.models import Article, Comment, Tag
from django.views import View
from django.views.generic import TemplateView, ListView


def get_tags(tags):
    result = []
    for tag in tags.split(','):
        clean_tag, _ = Tag.objects.get_or_create(name=tag)
        result.append(clean_tag)
    return result


def get_str_tags(queryset):
    return ','.join(([str(tag) for tag in queryset]))


class IndexView(ListView):
    template_name = 'article/index.html'
    model = Article
    context_object_name = 'articles'
    ordering = ['-created_at']
    paginate_by = 4
    paginate_orphans = 1
    page_kwarg = 'page'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = SimpleSearchForm()
        return context


class ArticleView(TemplateView):
    template_name = 'article/article.html'

    def get_context_data(self, **kwargs):
        pk = kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        context['article'] = get_object_or_404(Article, pk=pk)
        context['form'] = CommentInArticleForm()
        context['comments'] = Comment.objects.all().filter(article_id=pk).order_by('-created_at')
        return context


class ArticleCreateView(View):
    def get(self, request, *args, **kwargs):
        form = ArticleForm()
        return render(request, 'article/create.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article = Article.objects.create(
                title=form.cleaned_data['title'],
                author=form.cleaned_data['author'],
                text=form.cleaned_data['text'],
            )
            article.tags.set(get_tags(form.cleaned_data['tags']))
            return redirect('article_view', pk=article.pk)
        else:
            return render(request, 'article/create.html', context={'form': form})


class ArticleUpdateView(View):
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs['pk'])
        form = ArticleForm(data={
            'title': article.title,
            'text': article.text,
            'author': article.author,
            'tags': get_str_tags(article.tags.all())
        })
        return render(request, 'article/update.html', context={'form': form, 'article': article})

    def post(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs['pk'])
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article.title = form.cleaned_data['title']
            article.text = form.cleaned_data['text']
            article.author = form.cleaned_data['author']
            article.tags.set(get_tags(form.cleaned_data['tags']))
            article.save()
            return redirect('article_view', pk=article.pk)
        else:
            return render(request, 'article/update.html', context={'form': form, 'article': article})


class ArticleDeleteView(View):
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs['pk'])
        return render(request, 'article/delete.html', context={'article': article})

    def post(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs['pk'])
        article.delete()
        return redirect('index')