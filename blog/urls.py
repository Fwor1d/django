from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("blog/", views.post_list, name="post_list"),
    path("blog/create/", views.post_create, name="post_create"),
    path("blog/<int:pk>/", views.legacy_post_detail, name="legacy_post_detail"),
    path("blog/<int:year>/<int:month>/<int:day>/<slug:slug>/", views.post_detail, name="post_detail"),
    path("blog/<int:year>/<int:month>/<int:day>/<slug:slug>/edit/", views.post_edit, name="post_edit"),
    path("blog/<int:year>/<int:month>/<int:day>/<slug:slug>/delete/", views.post_delete, name="post_delete"),
]
