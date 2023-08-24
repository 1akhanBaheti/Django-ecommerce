from .views import auth_views
from django.urls import path
urlpatterns=[
    path('sign-up/',auth_views.sign_up.as_view()),
    path('sign-in/',auth_views.sign_in.as_view())
]