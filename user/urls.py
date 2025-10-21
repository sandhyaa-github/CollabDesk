from django.urls import path
from user.views import RegisterView, UserListView, UserRetrieveUpdateDelete

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('list/', UserListView.as_view(), name='user_list'),
    path('<int:pk>/', UserRetrieveUpdateDelete.as_view(),
         name="detail_update_delete")
]
