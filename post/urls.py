from django.urls import path
from post.views import CommentPost, CreatePost, GetPosts, LikePost, SharePost


urlpatterns = [
    path('create/',CreatePost.as_view(), name='create'),
    path('<int:post_id>/',CreatePost.as_view(), name='update Post'),
    path('/',GetPosts.as_view(), name='getPostById'),
    path('like/<int:post_id>/', LikePost.as_view(), name='like'),
    path('share/<int:post_id>/', SharePost.as_view(), name='share'),
    path('comment/<int:post_id>/', CommentPost.as_view(), name='get_comment_by_post_id'),
]
