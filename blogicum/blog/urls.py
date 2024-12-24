from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path(
        'posts/<int:post_id>/',
        views.post_detail,
        name='post_detail'
    ),
    path(
        'category/<slug:category_slug>/',
        views.category_posts,
        name='category_posts'
    ),
    path(
        'posts/create/',
        views.post_edit,
        name='create_post'
    ),
    path(
        'posts/<int:post_id>/edit/',
        views.post_edit,
        name='edit_post'
    ),
    path(
        'posts/<int:post_id>/delete/',
        views.post_delete,
        name='delete_post'
    ),
    path(
        'profile/<slug:username>/',
        views.Profile.as_view(),
        name='profile'
    ),
    path(
        'edit_profile/',
        views.edit_profile,
        name='edit_profile'
    ),
    path(
        'posts/<int:post_id>/add_comment/',
        views.add_comment,
        name="add_comment"
    ),
    path(
        'posts/<int:post_id>/edit_comment/<int:comment_id>/',
        views.edit_comment,
        name="edit_comment"
    ),
    path(
        'posts/<int:post_id>/delete_comment/<int:comment_id>/',
        views.delete_comment,
        name="delete_comment"
    )
]
