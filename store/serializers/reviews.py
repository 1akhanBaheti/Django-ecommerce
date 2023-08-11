from rest_framework import serializers
from ..models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','name','description','created_on']

    def create(self, validated_data):
       return Review.objects.create(product_id=self.context['product_id'],**validated_data)

         