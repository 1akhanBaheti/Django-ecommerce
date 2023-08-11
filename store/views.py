from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from store.serializers.product import ProductSerializer
from store.serializers.collection import CollectionSerializer
from store.serializers.reviews import ReviewSerializer
from .models import Product,Collection, Review
from rest_framework import status,generics
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
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


