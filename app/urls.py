from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout, name="logout"),
    path("sqlite/", views.sqlite_info, name="sqlite_info"),
    path("fuels/", views.fuels, name="fuels"),
    path("fuels/create/", views.fuel_create, name="fuel_create"),
    path("fuels/<int:fuel_id>/", views.fuel_detail, name="fuel_detail"),
    path("fuels/<int:fuel_id>/edit/", views.fuel_edit, name="fuel_edit"),
    path("fuels/<int:fuel_id>/delete/", views.fuel_delete, name="fuel_delete"),
    path("fuels/<int:fuel_id>/issue/", views.issue_fuel, name="issue_fuel"),
    path("fuel-types/", views.fuel_types, name="fuel_types"),
    path("fuel-types/create/", views.fuel_type_create, name="fuel_type_create"),
    path("fuel-types/<int:type_id>/edit/", views.fuel_type_edit, name="fuel_type_edit"),
    path("fuel-types/<int:type_id>/delete/", views.fuel_type_delete, name="fuel_type_delete"),
    path("issues/", views.issues, name="issues"),
    path("issues/create/", views.issue_create, name="issue_create"),
    path("issues/<int:issue_id>/edit/", views.issue_edit, name="issue_edit"),
    path("issues/<int:issue_id>/delete/", views.issue_delete, name="issue_delete"),
]
