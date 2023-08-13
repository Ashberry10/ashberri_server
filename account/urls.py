from account.modelapiview import FriendStatusAndCompatibility, FriendStatusAndCompatibilityById
from account.views import AllUser, UpdateUser, UserDeleteView, UserLoginView, UserProfileView,UserRegistrationView, uploadPost
from django.urls import path

from ashberri_server import settings
from ashberri_server import static

urlpatterns = [
    path('register/', UserRegistrationView.as_view(),name='register'),
    path('login/', UserLoginView.as_view(),name='login'),
    path('post/upload/',uploadPost.as_view(), name='upload'),
    path('getallusers/', AllUser.as_view(),name='getallusers'),
    path('getallusers/<int:id>',AllUser.as_view()),
    path('update/',UpdateUser.as_view(), name='user_update'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('friendStatusAndCompatibility/', FriendStatusAndCompatibility.as_view(), name='friend_status_and_compatibility'),
    path('friendStatusAndCompatibilityById/', FriendStatusAndCompatibilityById.as_view(), name='friendStatusAndCompatibilitById'),
    path('deleteuser/<int:id>', UserDeleteView.as_view(), name='user-delete'),
] 


# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)