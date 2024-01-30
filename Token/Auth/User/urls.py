from django.urls import path
from .views import Register , Login ,Userview , Refresh , Logout

urlpatterns = [
    path('', Register.as_view()),
    path('login', Login.as_view()),
    path('user', Userview.as_view()),
    path('refresh', Refresh.as_view()),
    path('logoutf', Logout.as_view()),
]