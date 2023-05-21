from django.urls import path
from .views import *
urlpatterns = [

    path('get_ranked_list/', get_ranked_list),
]