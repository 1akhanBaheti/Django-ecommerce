from rest_framework.viewsets import ModelViewSet
from ..serializers.reviews_serializers import ReviewSerializer


class ReviewView(ModelViewSet):
    serializer_class =ReviewSerializer
    
    def get_queryset(self):
        return ReviewSerializer.objects.filter(product=self.kwargs['product_pk'])
    def get_serializer_context(self):
        return {
            'product_id':self.kwargs['product_pk']
        }

