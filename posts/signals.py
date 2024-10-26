from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Post, Like

@receiver(post_save, sender=Like)
def add_likes_count(sender, instance, created, **kargs):
    if created:
        post = instance.post
        post.likes_count += 1
        post.save()

@receiver(post_delete, sender=Like)
def remove_likes_count(sender, instance, **kargs):
    post = instance.post
    post.likes_count -= 1
    post.save() 
