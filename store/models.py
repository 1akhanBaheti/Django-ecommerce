from django.db import models
from django.core.validators import MinValueValidator
from uuid import uuid4

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()

class Collection(models.Model):
    title =models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+')
    
    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(default='-')
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField(validators=[MinValueValidator(1)])
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion, blank=True)

class Cart(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid4)
    created_at =models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    product =models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity =models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1)
    ])

    class Meta:
        unique_together =[['cart','product']]


class Customer(models.Model):
    MEMBERSHIP_CHOICES =[
        ('B','Bronze'),
        ('S','Silver'),
        ('G','Gold'),
    ]
    first_name =models.CharField(max_length=255)
    last_name =models.CharField(max_length=255)
    email =models.EmailField(unique=True)
    phone =models.CharField(max_length=255)
    birth_date =models.DateField(null=True)
    membership= models.CharField(max_length=1,choices=MEMBERSHIP_CHOICES,default='B')

class Order(models.Model):
    PAYMENT_STATUS =[
        ('P','Pending'),
        ('C','Complete'),
        ('F','Failed'),
    ] 
    placed_at =models.DateTimeField(auto_now=True)
    # item = models.ForeignKey(Item,on_delete=models.CASCADE)
    customer =models.ForeignKey(Customer,on_delete=models.CASCADE)
    payment_status =models.CharField(max_length=1,choices=PAYMENT_STATUS,default='P')

class OrderItem(models.Model):
    order =models.ForeignKey(Order,on_delete=models.PROTECT)
    product =models.ForeignKey(Product,on_delete=models.PROTECT)
    quantity =models.IntegerField()
    unit_price =models.DecimalField(max_digits=6,decimal_places=2)

class Address(models.Model):
    street =models.CharField(max_length=255)
    city =models.CharField(max_length=255)
    customer =models.ForeignKey(Customer,on_delete=models.CASCADE)

class Review(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='review')
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
