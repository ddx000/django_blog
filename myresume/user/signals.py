from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

"""
https://docs.djangoproject.com/en/3.0/topics/signals/
1. post_save.connect(create_profile) - same as Qt
2. @receiver(post_save, sender= User)
Chinese annotation below
Django的訊號機制：
    提供一個低耦合的技術，當狀態改變時送出信號 觸發函式
    pre_save 物件save前觸發、post_save 物件save後觸發
    pre_delete 物件delete前觸發
Q: 為什麼要用鬆耦合技術:
    降低模組複雜度，盡量讓單元可以被抽換，系統大時，才不會彼此糾結，
    信號此處的機制和Qt很像，打出去根本沒有管有沒有人收到
"""

@receiver(post_save, sender= User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)

@receiver(post_save, sender= User)
def save_profile(sender, instance,**kwargs):
    instance.profile.save()