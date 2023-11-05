from django.urls import path

from . import views

urlpatterns = [
    path("", views.search_metadata_view, name="search_metadata"),
]