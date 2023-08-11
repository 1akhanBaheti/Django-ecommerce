from store.serializers.collection import CollectionSerializer
from .models import Collection
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import status

class ProductViews(APIView):

    def get(self,request):
        collection = Collection.objects.all().annotate(
            total_products = Count('product')
        )
        return Response(CollectionSerializer(collection,many=True).data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer =CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def patch(self,request,id):
        serializer =CollectionSerializer(data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

