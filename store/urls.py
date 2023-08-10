from . import views
from django.urls import path,include

urlpatterns= [
    path('products/',views.ProductListCreate.as_view()),
    path('products/<int:id>/',views.ProductRetrieveUpdateDestroy.as_view()),
    path('collections/', views.ProductRetrieveUpdateDestroy.as_view()),
    path('collections/<int:id>/',views.collection_detail)
]