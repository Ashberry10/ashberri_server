from django.urls import path
from post.views import CommentByID, CommentByPostID, Comments, CountLikesForPost, CreatePost, GetPostByUserID, GetPosts, LikePost, ListLikesForPost, SharePost


urlpatterns = [
    path('create/',CreatePost.as_view(), name='create'),
    path('<int:post_id>/',CreatePost.as_view(), name='update Post'),
    path('',GetPosts.as_view(), name='getPostById'),
    path('user/<int:user_id>',GetPostByUserID.as_view(), name='getAllPostsByUserId'),
    path('<int:post_id>/',CreatePost.as_view(), name='delete Post'),
    path('like/<int:post_id>/', LikePost.as_view(), name='like'),
    path('<int:post_id>/likes/', ListLikesForPost.as_view(), name='list-likes-for-post'),
    path('<int:post_id>/like-count/', CountLikesForPost.as_view(), name='count-likes-for-post'),
    path('share/<int:post_id>/', SharePost.as_view(), name='share'),
    path('comment/', Comments.as_view(), name='comment'), #create, get all
    path('comment/<int:comment_id>/', CommentByID.as_view(), name='get_comment_by_id'), #get by id , delete by id, update by id
    path('comment/post_id/<int:post_id>/', CommentByPostID.as_view(), name='get_comment_by_post_id'), # create, get all comment of a post by post_id

]
