from decimal import Decimal
from rest_framework import serializers
from rest_framework.fields import empty
from store.serializers.product import ProductSerializer
from ..models import Cart,CartItem,Product


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id','product','quantity','product_id']
        # read_only_fields=('quantity',)

    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True
    )

    def save(self, **kwargs):
        cartID = self.context['cart_id']
        if self.context['request'].method == 'PATCH':
            if not 'quantity' in self.validated_data:
                raise serializers.ValidationError({
                   "error": "quantity may not be null"
                })
            quantity =self.validated_data['quantity']
            item = CartItem.objects.get(cart_id=cartID,pk= self.context['cartitem_id'])
            if quantity ==0:
                self.instance=item.delete()
            else:
                item.quantity =quantity
                item.save()
                self.instance=item
            return self.instance

        quantity = self.validated_data['quantity']
        productID =  self.validated_data['product_id'].id
        self.validated_data['cart_id']=cartID
        self.validated_data['product_id']=productID
        try:
            item = CartItem.objects.get(cart_id=cartID,product_id=productID)
            item.quantity += quantity
            item.save()
            self.instance =item
        except CartItem.DoesNotExist:
            print(self.validated_data)
            self.instance= CartItem.objects.create(** self.validated_data)

        return self.instance
    

class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True,read_only=True)
    total_price =serializers.SerializerMethodField(method_name='get_total_price',read_only=True)

    def get_total_price(self,cart :Cart):
        items= cart.items.all()
        total=0
        for element in items:
            total += Decimal(element.quantity) * element.product.unit_price
        return total
    
    class Meta:
        model= Cart
        fields=['id','items','total_price']

