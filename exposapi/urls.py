from django.urls import path

from exposapi import views

urlpatterns = [
    path("", views.exposapi_view, name="exposapi_view"),
]
