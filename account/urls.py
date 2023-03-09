
# from account.views import UserPasswordResetView,UserRegistrationView,SendPasswordResetEmailView,UserLoginView,AllStudents,UserProfileView,UserChangePassword
from account.views import UserLoginView,UserRegistrationView,AllUser,UserProfileView, ModelapiView ,band_listing
from  account import views
from django.urls import path,include

urlpatterns = [
    path('register/', UserRegistrationView.as_view(),name='register'),
    path('login/', UserLoginView.as_view(),name='login'),
    path('getallusers/', AllUser.as_view(),name='getallusers'),
    # path('getalluserswithcomp/', AllUserwithComp.as_view(),name='getalluserswithcomp'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('Modelapi/',ModelapiView.as_view(), name='ModelapiView'),
    # path('course/<int:courseid>' ,views.courseDetails),
    path('band_listing/',band_listing.as_view(), name='band_listing'),
    # path('course/<int:courseid>/<int:secondid>' ,views.courseDetails)



   
    # path('changepassword/', UserChangePassword.as_view(), name='changepassword'),
    # path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
      # path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
]