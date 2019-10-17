from django import forms
from django.forms import widgets
from webapp.models import Category, Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['created_at', 'updated_at']


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