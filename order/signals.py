from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, OrderHistory


@receiver(post_save, sender=Order)
def create_order_history(sender, instance, created, **kwargs):
    if created:
        status = 'Created'
    else:
        if all([not instance.is_active, not instance.sent, not instance.received]):
            status = 'Canceled'
        elif instance.sent and instance.received:
            status = 'Complete'
        elif instance.sent:
            status = 'On the way'
        elif instance.is_active and not instance.sent:
            status = 'Awaiting shipment'

    OrderHistory.objects.create(order=instance, status=status)
