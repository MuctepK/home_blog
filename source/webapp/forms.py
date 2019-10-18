from django import forms
from django.forms import widgets
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
        for tag in self.cleaned_data['tags']:
            if not tag.strip():
                raise forms.ValidationError(message='Тег не может быть пустьм')
        return self.cleaned_data['tags']


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