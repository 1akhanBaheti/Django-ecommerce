from . import views
from django.urls import path,include
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('products',views.ProductView)
router.register('carts',views.CartView)

reviews_router = routers.NestedDefaultRouter(router,'products',lookup='product')
reviews_router.register('reviews',views.ReviewView, basename='product-reviews')

items_router =routers.NestedDefaultRouter(router,'carts',lookup='cart')
items_router.register('items',views.CartItemsView,basename='carts-items')

urlpatterns= [
    path('',include(router.urls)),
    path('',include(reviews_router.urls)),
    path('',include(items_router.urls)),
    path('collections/', views.CollectionListCreate.as_view()),
    path('collections/<int:id>/',views.CollectionRetrieveUpdateDestroy.as_view())
]