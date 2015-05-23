from django.db import models


class Photo(models.Model):
    photo = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    full_sent = models.BooleanField()
    full_sent_at = models.DateTimeField(blank=True, null=True)
    thumb_sent = models.BooleanField()
    thumb_sent_at = models.DateTimeField(blank=True, null=True)
