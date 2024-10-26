from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import User, Follow

@receiver(post_save, sender=Follow)
def add_followers_count(sender, instance, created, **kargs):
    if created:
        user = instance.following
        user.followers_count += 1
        user.save()

    
@receiver(post_delete, sender=Follow)
def remove_followers_count(sender, instance, **kargs):
    user = instance.following
    user.followers_count -= 1
    user.save()