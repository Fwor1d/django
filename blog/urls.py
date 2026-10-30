from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("create/", views.post_create, name="post_create"),
    path("<int:pk>/", views.legacy_post_detail, name="legacy_post_detail"),
    path("<int:year>/<int:month>/<int:day>/<slug:slug>/", views.post_detail, name="post_detail"),
    path("<int:year>/<int:month>/<int:day>/<slug:slug>/edit/", views.post_edit, name="post_edit"),
    path("<int:year>/<int:month>/<int:day>/<slug:slug>/delete/", views.post_delete, name="post_delete"),
]
