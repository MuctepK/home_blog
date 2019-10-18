from django.db.models import QuerySet, Q
from django.shortcuts import render, get_object_or_404, redirect
from webapp.forms import ArticleForm, CommentInArticleForm, SimpleSearchForm
from webapp.models import Article, Comment, Tag
from django.views import View
from django.views.generic import TemplateView, ListView


def get_or_create_tags(tags):
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

    def get(self, request, *args, **kwargs):
        self.form = SimpleSearchForm(data=request.GET)
        self.search_value = self.get_search_value()

        return super().get(request, *args, **kwargs)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            tag = self.search_value
            queryset = queryset.filter(
                Q(tags__name__iexact=tag)
            )
        return queryset

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
            article.tags.set(get_or_create_tags(form.clean_tags()))
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
            article.tags.clear()
            article.tags.set(get_or_create_tags(form.cleaned_data['tags']))
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