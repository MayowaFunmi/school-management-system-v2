from django.urls import path
from . import views

app_name = 'stats'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('get_table_data/', views.get_table_data, name='get_table_data'),
]