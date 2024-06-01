from django.contrib.auth.models import AbstractUser
from django.db import models
    
class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=10000)
    price = models.IntegerField()
    image = models.URLField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings")
    active = models.BooleanField(default=True)
    category = models.CharField(max_length=64, blank=True)
    def __str__(self):
        return f"{self.title} for {self.price} by {self.user}"
    
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="item_bids")
    value = models.IntegerField()

    def __str__(self):
        return f"Bid by {self.user} with {self.value} on {self.item}"
    

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="item_comments")
    comment = models.CharField(max_length=1000)

    def __str__(self):
        return f"Comment by {self.user} on {self.item}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watchlist")
    listings = models.ManyToManyField(Listing, blank=True, related_name="listing_watchlist")

    