from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
 
urlpatterns =[
    path('', views.home,name='home'),
    path('login/', views.loginPage,name='login'),
    path('viewcart/', views.viewcart,name='viewcart'),
    path('return_book/<int:pk>/', views.return_book, name='return_book'),
    path('addbook/', views.addbook,name='addbook'),
    path('delete_book/<int:pk>/delete/', views.delete_book,name='delete_book'),
    path('book_detail/<int:pk>/', views.book_detail, name='book_detail'),
    path('register/', views.registerPage,name='register'),
    path('logout/', views.logoutPage,name='logout'),
    path('addtocart/<str:pk>', views.addtocart,name='addtocart'),
    path('search/', views.search,name='search'),
    path('contact/', views.contact,name='contact'),
    path('mesaje/', views.mesaje,name='mesaje'),
    path('delete_mesaj/<int:pk>/', views.delete_mesaj,name='delete_mesaj'),
    path('top_books/', views.top_books,name='top_books'),
]


