from django.shortcuts import render, get_object_or_404, redirect
from webapp.forms import ArticleForm, CommentForm, CommentInArticleForm
from webapp.models import Article, Comment
from django.views import View
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'article/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.all()
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
                text=form.cleaned_data['text']
            )
            return redirect('article_view', pk=article.pk)
        else:
            return render(request, 'article/create.html', context={'form': form})


class ArticleUpdateView(View):
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs['pk'])
        form = ArticleForm(data={
            'title': article.title,
            'text': article.text,
            'author': article.author
        })
        return render(request, 'article/update.html', context={'form': form, 'article': article})

    def post(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs['pk'])
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article.title = form.cleaned_data['title']
            article.text = form.cleaned_data['text']
            article.author = form.cleaned_data['author']
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


class CommentView(TemplateView):
    template_name = 'comment/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.all().order_by('-created_at')
        return context


class CommentCreateView(View):
    def get(self, request, *args, **kwargs):
        form = CommentForm()
        return render(request, 'comment/create.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = CommentForm(data=request.POST)
        if form.is_valid():
            Comment.objects.create(
                author=form.cleaned_data['author'],
                text=form.cleaned_data['text'],
                article=form.cleaned_data['article']
            )

            return redirect('comment_index')
        else:
            return render(request, 'comment/create.html', context={'form': form})


class CommentUpdateView(View):
    def get(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs['pk'])
        form = CommentForm(data={
            'article': comment.article.pk,
            'text': comment.text,
            'author': comment.author
        })
        return render(request, 'comment/update.html', context={'form': form, 'comment': comment})

    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs['pk'])
        form = CommentForm(data=request.POST)
        if form.is_valid():
            Comment.objects.create(
                author=form.cleaned_data['author'],
                text=form.cleaned_data['text'],
                article=form.cleaned_data['article']
            )
            return redirect('comment_index')
        else:
            return render(request, 'comment/update.html', context={'form': form, 'comment': comment})


class CommentDeleteView(View):
    def get(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs['pk'])
        return render(request, 'comment/delete.html', context={'comment': comment})

    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs['pk'])
        comment.delete()
        return redirect('comment_index')


class CommentCreateInArticleView(View):
    def post(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk = kwargs['article_pk'])
        form = CommentInArticleForm(data=request.POST)
        print(article)
        if form.is_valid():
            Comment.objects.create(
                author=form.cleaned_data['author'],
                text=form.cleaned_data['text'],
                article=article
            )

            return redirect('article_view', pk=article.pk)
        else:
            context = {'comments': Comment.objects.all().filter(article_id=article.pk).order_by('-created_at'),
                        'form': form,
                       'article': article}
            return render(request, 'article/article.html', context)
