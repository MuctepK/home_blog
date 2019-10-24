from django.db.models import QuerySet, Q
from django.shortcuts import render, get_object_or_404, redirect
from webapp.forms import ArticleForm, CommentInArticleForm, SimpleSearchForm,FullSearchForm
from webapp.models import Article, Comment, Tag
from django.views import View
from django.views.generic import TemplateView, ListView, FormView


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
            tags = form.cleaned_data['tags']
            article.tags.set(self.get_or_create_tags(tags))
            return redirect('article_view', pk=article.pk)
        else:
            return render(request, 'article/create.html', context={'form': form})


    def get_or_create_tags(self,tags):
        result = []
        for tag in tags:
            clean_tag, _ = Tag.objects.get_or_create(name=tag)
            result.append(clean_tag)
        return result


    def get_str_tags(self,queryset):
        return ','.join(([str(tag) for tag in queryset]))


class ArticleUpdateView(View):
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs['pk'])
        form = ArticleForm(data={
            'title': article.title,
            'text': article.text,
            'author': article.author,
            'tags': self.get_str_tags(article.tags.all())
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
            tags = form.cleaned_data['tags']
            article.tags.set(self.get_or_create_tags(tags))
            article.save()
            return redirect('article_view', pk=article.pk)
        else:
            return render(request, 'article/update.html', context={'form': form, 'article': article})

    def get_or_create_tags(self,tags):
        result = []
        for tag in tags:
            clean_tag, _ = Tag.objects.get_or_create(name=tag)
            result.append(clean_tag)
        return result

    def get_str_tags(self,queryset):
        return ','.join(([str(tag) for tag in queryset]))

class ArticleDeleteView(View):
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs['pk'])
        return render(request, 'article/delete.html', context={'article': article})

    def post(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs['pk'])
        article.delete()
        return redirect('index')


class ArticleSearchView(FormView):
    template_name = 'article/search.html'
    form_class = FullSearchForm

    def form_valid(self, form):
        text = form.cleaned_data.get('text')
        query = Q()
        if text:
            in_title = form.cleaned_data.get('in_title')
            if in_title:
                query = query | Q(title__icontains=text)
            in_text = form.cleaned_data.get('in_text')
            if in_text:
                query = query | Q(text__icontains=text)
            in_tags = form.cleaned_data.get('in_tags')
            if in_tags:
                query = query | Q(tags__name__iexact=text)
            in_comment_text = form.cleaned_data.get('in_comment_text')
            if in_comment_text:
                query = query | Q(comments__text__icontains=text)
        author = form.cleaned_data.get('author')
        author_query = Q()
        if author:
            in_articles = form.cleaned_data.get('in_articles')
            if in_articles:
                author_query = author_query | Q(author__iexact=author)
            in_comments = form.cleaned_data.get('in_comments')
            if in_comments:
                author_query = author_query | Q(comments__author__iexact=author)
            if not text:
                query = author_query
        if author and text:
            query = query & author_query
        context = super().get_context_data(form=form)
        print(query)
        context['articles'] = Article.objects.filter(query).distinct()
        return self.render_to_response(context=context)
