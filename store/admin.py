from django.contrib import admin
from django.db.models import Count
from . import models
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.models import Group

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display= ['title','products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self,collection):
        url = reverse('admin:store_product_changelist') + f'?collection__id={collection.id}'
        return format_html('<a href="{}">{}</a>',url,collection.products_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count= Count('product')
        )


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display= ['title','unit_price','collection']
    list_editable = ['unit_price']
    list_filter = ['collection']

@admin.register(models.Profile)  #Decorator
class ProfileAdmin(admin.ModelAdmin):
    list_display= ['first_name','last_name','membership','phone','birth_date'] #Columns to display
    list_select_related=['user'] #To avoid extra queries

    def first_name(self,profile):
        return profile.user.first_name #Foriegn key relationship
    
    def last_name(self,profile):
        return profile.user.last_name  #Foriegn key relationship
