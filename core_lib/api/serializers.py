from rest_framework.serializers import HyperlinkedModelSerializer, SerializerMethodField
from rest_framework import serializers
from ..models import *

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

class GenreSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
        
class BookSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genres', 'image', 'quantity', 'rating', 'rented_at', 'due_date', 'total_orders' ]
        
    rating = SerializerMethodField()
    
    def get_rating(self, obj):
        return obj.rating
    
class RecenzieSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Recenzie
        fields = '__all__'
        
        
class CustomerSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        
class CartSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
        
class CartItemSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'
        
class ContactSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
