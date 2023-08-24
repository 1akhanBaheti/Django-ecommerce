from rest_framework import serializers

from store.models import Collection

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id','title',"total_products"]
    total_products = serializers.IntegerField(read_only=True)



def is_collection_exists(id):
    if isinstance(id,int):
        try:
            query= Collection.objects.get(pk=id)
            if query is Collection.DoesNotExist:
                return query
        except:
            raise serializers.ValidationError({
                    "error":"collection not found"
                })
    else:
        raise serializers.ValidationError({
                "error":"collection must be a integer"
        })



