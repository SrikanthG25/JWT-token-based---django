from django.urls import path
from .views import Register , Login , Userview , Logout

urlpatterns = [
    path('', Register.as_view()),
    path('login', Login.as_view()),
    path('user', Userview.as_view()),
    path('logout', Logout.as_view()),
]