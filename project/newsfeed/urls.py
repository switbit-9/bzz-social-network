from django.urls import path
from .views import *

app_name = 'feed'

urlpatterns = [
    path('create-post', PostCreateView.as_view(), name='home'),
    path('create-comment', create_comment, name='create-comment')
]