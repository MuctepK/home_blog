from django import forms
from django.forms import widgets, ValidationError
from webapp.models import Category, Article


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=200, label='Title', required=True)
    author = forms.CharField(max_length=40, label='Author', required=True)
    text = forms.CharField(max_length=3000, label='Text', required=True,
                           widget=widgets.Textarea)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label='Category',
                                      empty_label=None)
    tags = forms.CharField(max_length=256, label='Tags', required=False)

    def clean_tags(self):
        tags = []
        for tag in self.cleaned_data['tags'].split(','):
            if not tag.strip():
                raise ValidationError(message='Тег не может быть пустьм')
            tags.append(tag.strip())
        return tags


class CommentForm(forms.Form):
    article = forms.ModelChoiceField(queryset=Article.objects.all(), required=True, label='Article',
                                     empty_label=None)
    author = forms.CharField(max_length=40, required=False, label='Author', initial='Аноним')
    text = forms.CharField(max_length=400, required=True, label='Text',
                           widget=widgets.Textarea)


class CommentInArticleForm(forms.Form):
    author = forms.CharField(max_length=40, required=False, label='Author', initial='Аноним')
    text = forms.CharField(max_length=400, required=True, label='Text',
                           widget=widgets.Textarea)


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='Найти')


class FullSearchForm(forms.Form):
    text = forms.CharField(max_length=100, required=False, label='Текст')
    in_title = forms.BooleanField(initial=True, required=False, label='В заголовки')
    in_text = forms.BooleanField(initial=True, required=False, label='В тексте')
    in_tags = forms.BooleanField(initial=True, required=False, label='В тегах')
    in_comment_text = forms.BooleanField(initial=True, required=False, label='В тексте комментариев')
    author = forms.CharField(max_length=100, required=False, label='Автор')
    in_articles = forms.BooleanField(initial=True, required=False, label='В статьях')
    in_comments = forms.BooleanField(initial=True, required=False, label='В комментариеях')

    def clean(self):
        super().clean()
        text = self.cleaned_data.get('text')
        in_title = self.cleaned_data.get('in_title')
        in_text = self.cleaned_data.get('in_text')
        in_tags = self.cleaned_data.get('in_tags')
        in_comment_text = self.cleaned_data.get('in_comment_text')
        if text:
            if not (in_title or in_text or in_comment_text or in_tags):
                raise ValidationError(
                    "Один из чекбоксов для текста должен быть отмечен.",
                    code='no_text_search_destination')
        author = self.cleaned_data.get('author')
        in_articles = self.cleaned_data.get('in_articles')
        in_comments = self.cleaned_data.get('in_comments')
        if author:
            if not(in_articles or in_comments):
                raise ValidationError('Один из чекбоксов для автора должен быть отмечен.',
                                      code = 'no_author_search_destination')
        if not author and not text:
            raise ValidationError('Заполните хотя бы одно поле(поиск по автору или же по тексту?)',
                                  code='search_field_not_selected')
        return self.cleaned_data
