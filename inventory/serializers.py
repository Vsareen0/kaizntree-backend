from rest_framework import serializers
from .models import Item, Category, Tags


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['id', 'name', 'img']


class AddItemSerializer(serializers.ModelSerializer):
    in_stock = serializers.IntegerField(min_value=0)
    available_stock = serializers.IntegerField(min_value=0)
    
    class Meta:
        model = Item
        fields = ['id', 'sku', 'name', 'in_stock', 'available_stock', 'tags', 'category', 'user_id']

    def validate_in_stock(self, value):
        if value < 0:
            raise serializers.ValidationError('in_stock must be a non-negative value') 
        return value
    
    def validate_available_stock(self, value):
        if value < 0:
            raise serializers.ValidationError('available_stock must be a non-negative value')
        return value


class GetItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Item
        fields = ['id', 'sku', 'name', 'in_stock', 'available_stock', 'tags', 'category']


class DateRangeSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()