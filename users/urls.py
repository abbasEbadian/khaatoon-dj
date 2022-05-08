from django.urls import path
from . import views


urlpatterns = [
    path('authenticate/', views.authenticate),
    path('profile/', views.profile),

]