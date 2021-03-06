# Generated by Django 3.0.3 on 2020-03-08 13:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=400)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_listing', to='auctions.Listing')),
                ('owner', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='comment_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
