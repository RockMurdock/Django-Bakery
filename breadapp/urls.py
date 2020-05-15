from django.urls import path
from .views import *

app_name = "breadapp"

urlpatterns = [
    path('', bread_list, name='bread_list'),
    path('breads/form', bread_form, name='bread_form'),
    path('breads/<int:bread_id>', bread_details, name='bread_details')
]
