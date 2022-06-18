"""kurl_django_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include

from users.views.activate_user import ActivateUserAPIView
from users.views.register import RegisterUserAPIView
from users.views.user import UserViewSet
from users.views.user_list import UserListViewSet

urlpatterns = [
    path('register/', RegisterUserAPIView.as_view(), name='register'),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path(
        'activate/<slug:uidb64>/<slug:token>/',
        ActivateUserAPIView.as_view(), name='activate_user'
    ),
    path('users/', UserListViewSet.as_view({'get': 'list'}), name='user_list'),
    path('user/<int:pk>', UserViewSet.as_view({
        'get': 'retrieve',
        'patch': 'partial_update'
    }), name='user_detail'),
]
