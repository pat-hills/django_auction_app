# Generated by Django 3.1.1 on 2020-09-24 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auctioncomments_bid_watchlist'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AuctionComments',
            new_name='AuctionComment',
        ),
    ]
