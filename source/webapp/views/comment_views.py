from django.shortcuts import render, get_object_or_404, redirect
from webapp.forms import CommentForm, CommentInArticleForm
from webapp.models import Article, Comment
from django.views import View
from django.views.generic import TemplateView, ListView


class CommentView(ListView):
    template_name = 'comment/index.html'
    model = Comment
    context_key = 'comments'


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