from django.db import models

class Banner(models.Model):
    title = models.CharField(max_length=255, default="Default Banner")
    banner_image = models.ImageField(upload_to="banners/", null=True, blank=True)

    def __str__(self):
        return self.title

