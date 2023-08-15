from account.modelapiview import FriendStatusAndCompatibility, FriendStatusAndCompatibilityById
from account.views import AllUser, CommentPost, GetPosts, LikePost, SharePost, UpdateUser, UserDeleteView, UserLoginView, UserProfileView,UserRegistrationView, CreatePost
from django.urls import path



urlpatterns = [
    path('register/', UserRegistrationView.as_view(),name='register'),
    path('login/', UserLoginView.as_view(),name='login'),
    path('post/create/',CreatePost.as_view(), name='create'),
    path('post/<int:post_id>/',CreatePost.as_view(), name='update Post'),
    path('post/',GetPosts.as_view(), name='getPostById'),
    path('post/like/<int:post_id>/', LikePost.as_view(), name='like'),
    path('post/like/<int:post_id>/', LikePost.as_view(), name='like'),
    path('post/share/<int:post_id>/', SharePost.as_view(), name='share'),
    path('post/comment/<int:post_id>/', CommentPost.as_view(), name='comment'),
    path('post/comment/<int:post_id>/', CommentPost.as_view(), name='get_comment_by_post_id'),
    path('getallusers/', AllUser.as_view(),name='getallusers'),
    path('getallusers/<int:id>',AllUser.as_view()),
    path('update/',UpdateUser.as_view(), name='user_update'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('friendStatusAndCompatibility/', FriendStatusAndCompatibility.as_view(), name='friend_status_and_compatibility'),
    path('friendStatusAndCompatibilityById/', FriendStatusAndCompatibilityById.as_view(), name='friendStatusAndCompatibilitById'),
    path('deleteuser/<int:id>', UserDeleteView.as_view(), name='user-delete'),
] 

