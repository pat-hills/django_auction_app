# Generated by Django 3.1.1 on 2020-09-25 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_remove_watchlist_userwatchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidauction',
            name='notes',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
