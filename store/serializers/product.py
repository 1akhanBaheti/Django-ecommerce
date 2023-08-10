from decimal import Decimal
from rest_framework import serializers
from rest_framework.response import Response
from store.serializers.collection import CollectionSerializer, is_collection_exists
from ..models import Product,Collection
from django.shortcuts import get_object_or_404
from django.core.validators import MinValueValidator

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model =Product
        fields =['id','title','inventory','description', 'collection','price','price_with_tax']
    price = serializers.DecimalField(max_digits=6,decimal_places=2,source='unit_price')
    inventory = serializers.IntegerField(validators=[MinValueValidator(1)],write_only=True)
    price_with_tax = serializers.SerializerMethodField(method_name='get_price_with_tax',read_only=True,)
    collection = serializers.PrimaryKeyRelatedField(
        queryset = Collection.objects.all(),
        write_only=True
    )

    def get_price_with_tax(self,product:Product):
       return Decimal(format(Decimal((product.unit_price * Decimal(18/100)) + product.unit_price,),".2f"))

    def to_representation(self, instance):
        data= super().to_representation(instance)
        data['collection']=CollectionSerializer(instance.collection).data
        return data

        

           

        
    

    