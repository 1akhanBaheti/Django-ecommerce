from rest_framework import serializers
from ..models import User 


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields =['first_name','last_name','email','password']

    password= serializers.CharField(write_only=True,max_length=64, min_length=8)


class SignInSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    access_token = serializers.CharField(max_length=255,read_only=True)
    first_name = serializers.CharField(max_length=255,read_only=True)
    last_name = serializers.CharField(max_length=255,read_only=True)
    email = serializers.EmailField()
    password =serializers.CharField(max_length=64,write_only=True)
