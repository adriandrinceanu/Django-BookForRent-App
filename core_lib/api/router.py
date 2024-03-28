from rest_framework.routers import DefaultRouter
from .viewsets import *


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'genre', GenreViewSet)
router.register(r'book', BookViewSet)
router.register(r'recenzie', RecenzieViewSet)
router.register(r'customer', CustomerViewSet)
router.register(r'cart', CartViewSet)
router.register(r'cart-item', CartItemViewSet)
router.register(r'contact', ContactViewSet)



urls = router.urls