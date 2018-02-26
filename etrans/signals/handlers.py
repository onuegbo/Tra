from ..models import Profile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User



# basic syntax
# @receiver(<signal_to_listen_for_from_django_core_signals>,sender=<model_class_to_listen_to>)
# def method_with_logic_to_run_when_signal_is_emitted(sender, **kwargs):
# Logic when signal is emitted
# Access sender & kwargs to get info on model that emitted signal


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
