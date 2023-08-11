from . import views
from django.urls import path,include
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register( 'products',views.ProductView)

products_router = routers.NestedDefaultRouter(router,'products',lookup='product')
products_router.register('reviews',views.ReviewView, basename='product-reviews')

urlpatterns= [
    path('',include(router.urls)),
    path('',include(products_router.urls)),
    path('collections/', views.CollectionListCreate.as_view()),
    path('collections/<int:id>/',views.CollectionRetrieveUpdateDestroy.as_view())
]