from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    birthday = models.DateField("дата рождения", null=True, blank=True)
    bio = models.TextField("О себе", null=True, blank=True)
    image = models.ImageField("Аватарка", upload_to="profile_pics", blank=True)

    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self._meta.verbose_name_plural

    class Meta:
        verbose_name = "дополнительное поле"
        verbose_name_plural = "дополнительные поля"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()
