from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .models import *
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import *
import requests
from django.conf import settings
 
# Create your views here.

def home(request):
    books=Book.objects.all()
    genres = list(Genre.objects.all())
    genres.insert(0, 'All')  # Add 'All' as the first genre
    carts = Cart.objects.all()
    books_and_customers = {}
    for cart in carts:
        for book in cart.books.all():
            book_title = str(book)
            customer_name = str(cart.customer)
            due_date = book.due_date  # get the due date from the book model
            if book_title not in books_and_customers:
                books_and_customers[book_title] = [(customer_name, due_date)]
           
            else:
                books_and_customers[book_title].append((customer_name, due_date))
    context = {'books_and_customers': books_and_customers, 'books':books, 'genres': genres}
    if request.user.is_staff:
        return render(request,'core_lib/adminhome.html',context)
    else:    
        return render(request,'core_lib/home.html',context)


# def book_detail(request, pk):
#     try:
#         book = Book.objects.get(id=pk)
#         if request.method == 'POST':
#             form = RecenzieForm(request.POST)
#             if form.is_valid():
#                 recenzie = form.save(commit=False)
#                 recenzie.user = request.user  # set the current user
#                 recenzie.book = book  # set the current book
#                 recenzie.save()
#                 return redirect('book_detail', pk=book.id)  # redirect to the current book detail view
#         else:
#             form = RecenzieForm()
#         context = {
#             'form': form,
#             'book': book,
#             'user': request.user  # add current user to context
#         }
#     except Book.DoesNotExist:
#         return HttpResponse("404")
#     return render(request, 'core_lib/book_detail.html', context)


def book_detail(request, pk):
    try:
        book = Book.objects.get(id=pk)
        if request.method == 'POST':
            form = RecenzieForm(request.POST)
            if form.is_valid():
                recenzie = form.save(commit=False)
                recenzie.user = request.user  # set the current user
                recenzie.book = book  # set the current book
                recenzie.save()
                return redirect('book_detail', pk=book.id)  # redirect to the current book detail view
        else:
            form = RecenzieForm()

        # Fetch the YouTube trailer
        api_key = settings.API_KEY
        response = requests.get(f'https://www.googleapis.com/youtube/v3/search?part=snippet&q="%{book.title}%20trailer"&key={api_key}')
        data = response.json()
        youtube_video_id = None
        if data['items']:
            for item in data['items']:
                if 'videoId' in item['id']:
                    youtube_video_id = item['id']['videoId']
                    break

        context = {
            'form': form,
            'book': book,
            'user': request.user,  # add current user to context
            'youtube_video_id': youtube_video_id,  # add YouTube video ID to context
        }
    except Book.DoesNotExist:
        return HttpResponse("404")
    return render(request, 'core_lib/book_detail.html', context)
 
def logoutPage(request):
    logout(request)
    return redirect('/')
 
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
       if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            print("working")
            login(request,user)
            return redirect('/')
       context={}
       return render(request,'core_lib/login.html',context)
 
def registerPage(request):
    form=CreateUserForm()
    cust_form=CreateCustomerForm()
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        cust_form=CreateCustomerForm(request.POST)
        if form.is_valid() and cust_form.is_valid():
            user=form.save()
            customer=cust_form.save(commit=False)
            customer.user=user 
            customer.save()
            return redirect('/')
    context={
        'form':form,
        'cust_form':cust_form,
    }
    return render(request,'core_lib/register.html',context)
 
def addbook(request):
    form = CreateBookform()
    if request.method == 'POST':
        form = CreateBookform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            print(form.errors)  # Print form errors, in caz ca exista
    context = {'form': form}
    return render(request, 'core_lib/addbook.html', context)
 




def viewcart(request):
    cust = Customer.objects.filter(user=request.user)
    for c in cust:
        carts = Cart.objects.filter(customer=c)
        for cart in carts:
            if cart.books.count() > 0:  # Check if the cart is not empty
                context = {
                    'cart': cart
                }
                return render(request, 'core_lib/viewcart.html', context)
    # If no non-empty cart was found, render the 'emptycart.html' template
    return render(request, 'core_lib/emptycart.html')



 
def addtocart(request,pk):
    book=Book.objects.get(id=pk)
    book.increment_orders
    cust=Customer.objects.filter(user=request.user)
    book.save()
    for c in cust:       
        carts=Cart.objects.all()
        reqcart=''
        for cart in carts:
            if(cart.customer==c):
                reqcart=cart
                break
        if(reqcart==''):
            reqcart=Cart.objects.create(
                customer=c,
            )
        reqcart.books.add(book)
        book.quantity -= 1  # Decrement the book's quantity
        book.rented_at = timezone.now()  # Set the rented_at field to the current time
        book.due_date = timezone.now() + timedelta(days=1)  # Set the due date to 1 day from now
        book.save()    
    return redirect('viewcart')


def return_book(request, pk):
    book = Book.objects.get(id=pk)
    cust = Customer.objects.filter(user=request.user)
    for c in cust:
        carts = Cart.objects.all()
        for cart in carts:
            if cart.customer == c:
                if book in cart.books.all():  # Check if the book is in the cart
                    cart.books.remove(book)  # Remove the book from the cart
                    book.quantity += 1  # Increment the book's quantity
                    book.save()
                    break
    return redirect('viewcart')

def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect('home')

def search(request):
    books = Book.objects.none()  # Define books as an empty queryset
    if request.method == 'GET': 
        form = BookSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['search']
            books = Book.objects.filter(title__icontains=query) | Book.objects.filter(author__icontains=query) | \
                    Book.objects.filter(genres__name__icontains=query)
    else:
        form = BookSearchForm()
    context = {'form': form, 'books': books}
    return render(request, 'core_lib/search.html', context)


# def contact(request):
#     form = ContactForm()
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             subiect = form.cleaned_data['subiect']
#             nume = form.cleaned_data['nume']
#             email = form.cleaned_data['email']
#             mesaj = form.cleaned_data['mesaj']
#             rented_books = form.cleaned_data['rented_books']
#             liked_books = form.cleaned_data['liked_books']
#             form.save()
#             send_mail(subject=subiect, message=mesaj, from_email='drinceanuadrian@gmail.com',  html_message=nume+rented_books+liked_books, recipient_list=[email])
#             return redirect('contact')
#         else:
#             print(form.errors)  # Print form errors, in caz ca exista
#     context = {'form': form}
#     return render(request, 'core_lib/contact.html', context)



def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subiect = form.cleaned_data['subiect']
            nume = form.cleaned_data['nume']
            email = form.cleaned_data['email']
            mesaj = form.cleaned_data['mesaj']
            rented_books = form.cleaned_data['rented_books']
            liked_books = form.cleaned_data['liked_books']
            form.save()

            # Create the HTML message from a template
            html_message = render_to_string('core_lib/email_template.html', {
                'nume': nume,
                'mesaj': mesaj,
                'rented_books': rented_books,
                'liked_books': liked_books,
            })

            # Create the email and attach the HTML message
            email = EmailMultiAlternatives(
                subject=subiect,
                body=mesaj,  # this can be the same as `mesaj` or a simplified version
                from_email='adrian@bookforrent.com',
                to=[email],
            )
            email.attach_alternative(html_message, 'text/html')
            email.send()
            messages.success(request, 'Your message has been sent.')
            return redirect('contact')
        else:
            print(form.errors)  # Print form errors, in caz ca exista
    context = {'form': form}
    return render(request, 'core_lib/contact.html', context)


def mesaje(request):
    all_messages = Contact.objects.all()
    return render(request, 'core_lib/mesaje.html', {'all_messages': all_messages})

def delete_mesaj(request, pk):
    mesaj = get_object_or_404(Contact, pk=pk)
    mesaj.delete()
    return redirect('mesaje')

def top_books(request):
    books = Book.objects.all().order_by('-total_orders')
    return render(request, 'core_lib/top_books.html', {'books': books})
