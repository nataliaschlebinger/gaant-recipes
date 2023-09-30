from django.urls import path

from . import views

app_name="recipes"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:recipe_id>/", views.detail, name="detail"),
    path("<int:recipe_id>/edit", views.edit, name="edit"),
    path("create/", views.create, name="create"),
    path("<str:recipe_id>/submit", views.submit, name="submit"),
    path("<int:recipe_id>/delete", views.delete, name="delete"),
]
