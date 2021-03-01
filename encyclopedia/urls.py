from django.urls import path

from . import views

app_name: "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.article, name="article"),
    path("wiki/search/", views.search, name="search")
]