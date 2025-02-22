from django.db import models


class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    link = models.URLField()

    def __str__(self):
        return f"{self.title} by {self.artist}"


class SpotiEx(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    link = models.URLField()

    def __str__(self):
        return f"{self.title} by {self.artist}"


class SpotiNoex(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    link = models.URLField()

    def __str__(self):
        return f"{self.title} by {self.artist}"
