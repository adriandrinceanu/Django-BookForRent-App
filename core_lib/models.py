from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Sum
 
# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


def get_default_due_date():
    return timezone.now() + timedelta(days=1)


class Book(models.Model):
    title=models.CharField(max_length=200,null=True)
    author=models.CharField(max_length=200,null=True)
    genres = models.ManyToManyField(Genre)
    image = models.ImageField(upload_to='book_images/')
    quantity = models.IntegerField(default=0)
    rented_at = models.DateTimeField(auto_now_add=True, null=True)
    due_date = models.DateTimeField(default=get_default_due_date)
    total_orders = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.id:  # if the book is rented for the first time
            self.due_date = datetime.now() + timedelta(days=1)  # set the due date to 1 day from now
        super().save(*args, **kwargs)
        
 
    def __str__(self):
        return str(self.title)
    
    
    @property
    def rating(self):
        rating = 0
        recenzii = self.recenzie_set.all()
        for recenzie in recenzii:
            rating +=recenzie.rating
        try:
            return rating / len(recenzii)
        except ZeroDivisionError:
            return 0
    @property   
    def increment_orders(self):
        self.total_orders += 1
        self.save()
    

    

class Recenzie(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1)
    titlu = models.CharField(max_length=100)
    descriere = models.CharField(max_length=100)

 
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name=models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=200,null=True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    
    def __str__(self):
        return str(self.name)
 
class Cart(models.Model): 
    customer=models.OneToOneField(Customer, null=True, on_delete=models.CASCADE) 
     # Old books field
    books = models.ManyToManyField(Book, through='CartItem')
    # New books field referencing CartItem
    # books = models.ForeignKey('CartItem', on_delete=models.CASCADE, null=True, blank=True, related_name='books_ordered_by_cart')  
    
 
    def __str__(self):
        return str(self.customer)
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity_ordered = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.book.title} - {self.quantity_ordered}"

RENT_CHOICES = [
    ('yes', 'Yes'),
    ('no', 'No'),
]   
    
class Contact(models.Model):
    nume = models.CharField(max_length=100)
    email = models.EmailField()
    rented = models.CharField(max_length=3, choices=RENT_CHOICES, blank=True, null=True)
    rented_books = models.CharField(max_length=200, null=True, blank=True)
    liked_books = models.CharField(max_length=200, null=True, blank=True)
    subiect = models.CharField(max_length=255)
    mesaj = models.TextField(max_length=1000)
    
    

