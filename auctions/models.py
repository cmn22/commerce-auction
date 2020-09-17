from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.username}"

class Listing(models.Model):
    CATEGORIES = [
        ('Fashion', 'Fashion'),
        ('Furniture', 'Furniture'),
        ('Electronics', 'Electronics'),
        ('Collectibles', 'Collectibles'),
        ('Games & Toys', 'Games & Toys'),
        ('Motor Vehicle', 'Motor Vehicle'),
        ('Property', 'Property'),
        ('None', 'None')
    ]
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=1000)
    base_price = models.IntegerField()
    current_price = models.IntegerField()
    image = models.URLField()
    category = models.CharField(max_length=20, choices=CATEGORIES, default='NONE')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items_owned")
    active = models.BooleanField()
    date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.title} by {self.owner.username}"

class Bid(models.Model):
    bid = models.IntegerField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids_on")
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"Rs. {self.bid} bid on {self.item.title} by {self.bidder.username}"

class Comment(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="list_comments")
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments_made")
    comment = models.TextField(max_length=1000)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.commenter.username}'s comment on {self.item.title}"

class Watchlist(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="users_wished")
    wisher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items_wished")

    def __str__(self):
        return f"{self.wisher.username} wishes {self.item.title}"
