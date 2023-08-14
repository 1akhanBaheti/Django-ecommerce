from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.decorators import api_view
from store.serializers.cart import CartSerializer, CartItemSerializer
from store.serializers.product import ProductSerializer
from store.serializers.collection import CollectionSerializer
from store.serializers.reviews import ReviewSerializer
from .models import Product,Collection, Review, Cart, CartItem
from rest_framework import status,generics
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import ListModelMixin

class ProductView(ModelViewSet):
    queryset =Product.objects.select_related('collection').all()
    serializer_class =ProductSerializer

    def delete(self, request, id):
        product= get_object_or_404(Product,pk=id)
        print(product.orderitem_set.count())
        if product.orderitem_set.count() >0:
            return Response({
                "error":"Product cannot be deleted"
            })
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ReviewView(ModelViewSet):
    serializer_class =ReviewSerializer
    
    def get_queryset(self):
        return Review.objects.filter(product=self.kwargs['product_pk'])
    def get_serializer_context(self):
        return {
            'product_id':self.kwargs['product_pk']
        }

class CartView(GenericViewSet,mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin,mixins.UpdateModelMixin):
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

class CollectionListCreate(generics.ListCreateAPIView):
    queryset =Collection.objects.all().annotate(
            total_products = Count('product')
        )
    serializer_class =CollectionSerializer

class CollectionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg='id'
    queryset =Collection.objects.all().annotate(
            total_products = Count('product')
        )
    serializer_class =CollectionSerializer


