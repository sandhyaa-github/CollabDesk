from django.urls import path
from user.views import RegisterView, UserListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('list/', UserListView.as_view(), name='user_list'),
]
