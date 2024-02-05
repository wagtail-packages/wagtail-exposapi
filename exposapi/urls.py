from django.urls import include, path
from exposapi import views

urlpatterns = [
    path("", views.exposapi_view, name="exposapi_view"),
]
