from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Book, CartItem

@receiver(post_save, sender=CartItem)
def update_book_quantity(sender, instance, created, **kwargs):
    book = instance.book
    quantity = instance.quantity_ordered

    if created:
        book.quantity -= quantity
    else:
        previous_order_quantity = instance._old_values['quantity_ordered']
        book.quantity -= quantity + previous_order_quantity

    book.save()


@receiver(post_delete, sender=CartItem)
def restock_book(sender, instance, **kwargs):
    book = instance.book
    quantity = instance.quantity_ordered

    book.quantity += quantity
    book.save()