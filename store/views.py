from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from store.serializers.product import ProductSerializer
from store.serializers.collection import CollectionSerializer
from .models import Product,Collection
from rest_framework import status,generics
from django.db.models import Count

class ProductListCreate(generics.ListCreateAPIView):
    queryset =Product.objects.select_related('collection').all()
    serializer_class =ProductSerializer

class ProductRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg='id'
    queryset =Product.objects.select_related('collection').all()
    serializer_class =ProductSerializer

@api_view(['GET','DELETE','PATCH'])
def product_detail(request,id):
    product = get_object_or_404(Product,pk=id)
    if request.method =='GET':
        return Response(ProductSerializer(product).data)
    elif request.method =='DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method =='PATCH':
        serializer = ProductSerializer(product,data=request.data,partial=True,context={
            "request":request
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)

@api_view(['GET','PATCH','DELETE'])
def collection_detail(request,id) :
    collection = get_object_or_404(Collection,pk=id)
    collection.total_products = Collection.objects.filter(pk=id).aggregate(count=Count('product'))['count']
    if request.method =='GET':
        return Response(CollectionSerializer(collection).data)
    elif request.method =='PATCH':
        serializer = CollectionSerializer(collection,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        Response({
            "error":"method not allowed"
        },status=status.HTTP_405_METHOD_NOT_ALLOWED)


    
@api_view(['GET','POST'])
def list_collections(request):
    if request.method =='GET':
        collection = Collection.objects.all().annotate(
            total_products = Count('product')
        )
        return Response(CollectionSerializer(collection,many=True).data,status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer =CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    else:
        return Response({
            "error":"method not allowed"
        },status=status.HTTP_405_METHOD_NOT_ALLOWED)

