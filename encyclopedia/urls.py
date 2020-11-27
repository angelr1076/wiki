from django.urls import path
from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.entry, name="entry"),
    path("wiki/", views.search, name="search"),
    path("new/", views.new, name="new"),
    path("wiki/<str:title>/edit/", views.edit, name="edit"),
    path("random/", views.random_page, name="random"),
]
