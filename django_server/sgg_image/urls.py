from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('perform_sgg_image/', views.perform_sgg_image_api),
    path('translate_to_human_read/', views.translate_to_human_read_api),
]
