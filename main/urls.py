from django.urls import path
from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("search", views.search, name="search"),
	path("finance", views.finance, name="finance"),
	path("singapore", views.singapore, name="singapore")
]