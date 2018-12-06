
from django.urls import path

from .views import HomePage, ValideXML

urlpatterns = [
    path('', HomePage.as_view(), name='home-view'),
    path('validators', ValideXML.as_view(), name='validators-view'),
]
