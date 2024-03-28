from typing import Any
from django.forms import ModelForm
from django import forms
from .models import Book, Customer, Recenzie, Contact
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
 
class CreateUserForm(UserCreationForm):
    
    class Meta:
        model=User
        fields=['username'] 
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        
 
class CreateCustomerForm(ModelForm):
    
    class Meta:
        model=Customer
        fields= ['name', 'email']
        exclude=['user']
        widgets = {
            'name' : forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Numele tau'
            }),
            'email' : forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Emailul tau'
            }),
        }
 
class CreateBookform(ModelForm):
    class Meta:
        model=Book
        fields=['title', 'author', 'genres', 'image', 'quantity']
        exclude = ['due_date', 'total_orders']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Title'
                }),
            'author': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Author'
                }),
            'genres': forms.SelectMultiple(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Select genre'
                }),
            'image': forms.ClearableFileInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Select Image'
                }),
            'quantity': forms.NumberInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Quantity'
                })
            
        }
        
        
class BookSearchForm(forms.Form):
    search = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type a book title'}))
    
class RecenzieForm(ModelForm):
    class Meta:
        model=Recenzie
        fields=['rating', 'titlu', 'descriere']
        
class ContactForm(ModelForm):
    RENT_CHOICES = [('yes', 'Yes'), ('no', 'No')]
    rented = forms.ChoiceField(choices=RENT_CHOICES, widget=forms.RadioSelect(attrs={'class': 'form-check-input '}), required=False,\
                label="Did you rent any books from us?")
    rented_books = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'display:none'}),\
                label="What book/books did you rent?")
    liked_books = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'display:none'}),\
                label="Did you liked them?")

    class Meta:
        model = Contact
        fields=['nume', 'email', 'rented', 'rented_books', 'liked_books', 'subiect', 'mesaj'] 
        widgets = {
            'nume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nume'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'subiect': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subiect'}),
            'mesaj': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Mesajul tau'}),
        }