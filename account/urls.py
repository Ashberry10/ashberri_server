from account.views import UserPasswordResetView,UserRegistrationView,SendPasswordResetEmailView,UserLoginView,AllStudents,UserProfileView,UserChangePassword
from django.urls import path,include

urlpatterns = [
    path('register/', UserRegistrationView.as_view(),name='register'),
    path('login/', UserLoginView.as_view(),name='login'),
    path('getallusers/', AllStudents.as_view(),name='getallusers'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePassword.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
      path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
]