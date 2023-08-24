from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models import Product
from ..serializers.product_serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser

class customPagination(PageNumberPagination):
    page_size =10


class ProductView(ModelViewSet):
    queryset =Product.objects.select_related('collection').all()
    serializer_class =ProductSerializer
    pagination_class = customPagination

    def get_permissions(self):
        print(self.request)
        if self.request.method =='GET':
            return []
        return [IsAuthenticated(),IsAdminUser()]
    
    def get_authenticators(self):
        if self.request.method == 'GET':
            return []
        return super().get_authenticators()

    def delete(self, request, id):
        product= get_object_or_404(Product,pk=id)
        print(product.orderitem_set.count())
        if product.orderitem_set.count() >0:
            return Response({
                "error":"Product cannot be deleted"
            })
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)