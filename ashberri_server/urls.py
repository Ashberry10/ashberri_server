"""
URL configuration for ashberri_server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from chat.views import SendMessageView,GetMessageView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('friend/', include('friend.urls')),
    path('account/',include('account.urls')),
    path('post/', include('post.urls')),
    path('search/', include('customsearch.urls')),
    path('send-message/', SendMessageView.as_view(), name='send-message'),
    # path('view-messages/', ViewMessagesView.as_view(),name='view-messages'),
    path('get-messages/', GetMessageView.as_view(),name='get-messages')
# ]
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)