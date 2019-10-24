from django.contrib import admin
from django.urls import path
from webapp.views import IndexView, ArticleView, ArticleCreateView, ArticleUpdateView, \
    ArticleDeleteView, CommentView, CommentCreateView, CommentUpdateView, CommentDeleteView, CommentCreateInArticleView,\
    ArticleSearchView

urlpatterns = [
path('', IndexView.as_view(), name='index'),
    path('article/<int:pk>/', ArticleView.as_view(), name='article_view'),
    path('article/add/', ArticleCreateView.as_view(), name='article_add'),
    path('article/<int:pk>/update/', ArticleUpdateView.as_view(), name='article_update'),
    path('article/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    path('article/search/', ArticleSearchView.as_view(), name='article_search'),
    path('comments/', CommentView.as_view(), name='comment_index'),
    path('comment/add/', CommentCreateView.as_view(), name='comment_add'),
    path('comment/update/<int:pk>', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/delete/<int:pk>', CommentDeleteView.as_view(), name='comment_delete'),
    path('comment/add/<int:article_pk>', CommentCreateInArticleView.as_view(), name='comment_create_in_article')
    ]