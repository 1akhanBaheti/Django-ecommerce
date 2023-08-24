from .views import product_views,reviews_views,cart_views,collection_views,Profile_views
from django.urls import path,include
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('products',product_views.ProductView)
router.register('carts',cart_views.CartView)

reviews_router = routers.NestedDefaultRouter(router,'products',lookup='product')
reviews_router.register('reviews',reviews_views.ReviewView, basename='product-reviews')

items_router =routers.NestedDefaultRouter(router,'carts',lookup='cart')
items_router.register('items',cart_views.CartItemsView,basename='carts-items')

urlpatterns= [
    path('',include(router.urls)),
    path('',include(reviews_router.urls)),
    path('',include(items_router.urls)),
    path('collections/', collection_views.CollectionListCreate.as_view()),
    path('collections/<int:id>/',collection_views.CollectionRetrieveUpdateDestroy.as_view()),
    path('users/me/',Profile_views.ProfileView.as_view()),
]