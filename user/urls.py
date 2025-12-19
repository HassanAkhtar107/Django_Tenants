from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import SignupView, LoginView, ProfileView, LogoutView, UserListView, UserUpdateView, ClientList
urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('userList/', UserListView.as_view(), name='userList'),
    path('userUpdate/<int:pk>/', UserUpdateView.as_view(), name='userUpdate'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('clientList/', ClientList.as_view(), name='Client_List'),
]