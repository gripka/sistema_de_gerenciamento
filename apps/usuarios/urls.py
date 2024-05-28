from django.urls import path
from . import views


app_name = 'usuarios'

urlpatterns = [
    path('login/', views.login_view, name='login'),  # Certifique-se de que o nome da URL é 'login'
    path('logout/', views.logout_view, name='logout'),  # Use o novo nome da view
    path('recuperar-senha/', views.recuperar_senha, name='recuperar_senha'),
]