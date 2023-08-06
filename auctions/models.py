from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name=models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name}'


class Bid(models.Model):
    buyer=models.ForeignKey(User, related_name='bidding', on_delete=models.CASCADE)
    bid_price=models.FloatField()
    
    def __str__(self):
        return f"{self.bid_price} bid by {self.buyer}"




class Listing(models.Model):
    title=models.CharField(max_length=100)
    description=models.CharField(max_length=1000)
    imageUrl=models.CharField(max_length=1000)
    initial_bid=models.ForeignKey(Bid, on_delete=models.CASCADE,related_name='product')
    activity=models.BooleanField(default=True)
    seller=models.ForeignKey(User, on_delete=models.CASCADE, related_name='listing')
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    watchlist=models.ManyToManyField(User, blank=True, null=True, related_name='listing_watchlist')

    def __str__(self):
        return f'{self.title}'



class Comments(models.Model):
    username=models.ForeignKey(User, related_name='review', on_delete=models.CASCADE)
    text=models.CharField(max_length=100)
    forListing=models.ForeignKey(Listing, related_name='item', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.username} : {self.text}"