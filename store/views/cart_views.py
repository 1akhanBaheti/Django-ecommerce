from rest_framework.viewsets import GenericViewSet,ModelViewSet
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin
from ..models import Cart,CartItem
from ..serializers.cart_serializers import CartSerializer,CartItemSerializer


class CartView(GenericViewSet,CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin):
    queryset = Cart.objects.prefetch_related('items__product__collection').all()
    serializer_class = CartSerializer

class CartItemsView(ModelViewSet):
    serializer_class = CartItemSerializer
    http_method_names =['get','post','patch','delete']
    def get_queryset(self):
        return CartItem.objects.filter(cart=self.kwargs['cart_pk']).select_related('product__collection').all()
    
    def get_serializer_context(self):
        if not 'pk' in self.kwargs:
            self.kwargs['pk']=-1
       
        return {
            'cart_id':self.kwargs['cart_pk'],
            'cartitem_id':self.kwargs['pk'],
            'request':self.request

            }