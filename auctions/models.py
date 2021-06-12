from typing import List
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields.related import RelatedField
from django.utils import timezone


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=200)
    starting_bid = models.FloatField()
    url_image = models.URLField(max_length=1000, null=True, blank=True)
    category = models.CharField(max_length=64, null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sales")
    status = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=SET_NULL, null=True)

    def __str__(self):
        return f"{self.seller} : {self.title}"


class Bid(models.Model):
    amount = models.FloatField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="offers_made")
    listing = models.ForeignKey(Listing, on_delete=CASCADE, related_name="auctions", blank=True, null=True)

    def __str__(self):
        return f"{self.bidder} : {self.amount}"  


class Comment(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments_made")
    comment = models.CharField(max_length=100)
    date_created = models.DateField(auto_now_add=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="users_comments", blank=True, null=True)

    def __str__(self):
        return f"{self.user_name} : {self.comment}"