from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Auction(models.Model):
    item_name = models.CharField(max_length=128)
    item_title = models.CharField(max_length=128)
    item_bid_price = models.FloatField(max_length=128)
    item_bid_initial = models.FloatField(max_length=128,null=True)
    item_description = models.CharField(max_length=256)
    item_category = models.CharField(max_length=128)
    item_image_url = models.FileField(upload_to='images/', null=True, verbose_name="")
    date_created = models.DateField(null=False, blank=False, auto_now=True)
    is_deleted = models.BooleanField(default=False)
    is_sold = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,related_name="user")

    def __str__(self):
         return "%s %s" % (self.item_name,self.item_bid_price)


class Bidding(models.Model):
    bid_amount = models.FloatField(max_length=128)
    date_created = models.DateTimeField(null=False, blank=False, auto_now=True)
    is_deleted = models.BooleanField(default=False)
    notes = models.CharField(max_length=256,null=True)
    auctionedby = models.CharField(max_length=256,null=True)
    auctionbid = models.ForeignKey('Auction', on_delete=models.CASCADE, blank=True,related_name="auctionbid")
    userb = models.ForeignKey('User', on_delete=models.CASCADE,null=True, blank=True,related_name="userb")

    def __str__(self):
        return f"{self.id} {self.bid_amount}"
         
class Watchlist(models.Model):
    date_created = models.DateTimeField(null=False, blank=False, auto_now=True)
    is_deleted = models.BooleanField(default=False)
    notes = models.CharField(max_length=256)
    auctionbw = models.ForeignKey('Auction', null=True, on_delete=models.CASCADE, blank=True,related_name="auctionbw")
    userw = models.ForeignKey('User', on_delete=models.CASCADE,null=True, blank=True,related_name="userw")

    def __str__(self):
         return "%s %s" % (self.id,self.notes)


 

class Comments(models.Model):
    title = models.CharField(max_length=256)
    comments = models.CharField(max_length=256)
    date_created = models.DateTimeField(null=False, blank=False, auto_now=True)
    is_deleted = models.BooleanField(default=False)
    auctionbc = models.ForeignKey('Auction', on_delete=models.CASCADE,null=True, blank=True,related_name="auctionbc")
    userc = models.ForeignKey('User', on_delete=models.CASCADE,null=True, blank=True,related_name="userc")

    def __str__(self):
         return "%s %s" % (self.title,self.comments)