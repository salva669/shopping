from rest_framework import serializers
from .models import Bidhaas, Sale, SaleItem, Customer

class BidhaaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bidhaas
        fields = '__all__'

class SaleItemSerializer(serializers.ModelSerializer):
    bidhaa_name = serializers.CharField(source='bidhaa.jina', read_only=True)
    
    class Meta:
        model = SaleItem
        fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True, read_only=True)
    sold_by_username = serializers.CharField(source='sold_by.username', read_only=True)
    
    class Meta:
        model = Sale
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'