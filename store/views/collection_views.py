from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from django.db.models import Count
from ..serializers.collection_serializers import CollectionSerializer
from ..models import Collection

class CollectionListCreate(ListCreateAPIView):
    queryset =Collection.objects.all().annotate(
            total_products = Count('product')
        )
    serializer_class =CollectionSerializer

class CollectionRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg='id'
    queryset =Collection.objects.all().annotate(
            total_products = Count('product')
        )
    serializer_class =CollectionSerializer
