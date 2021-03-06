# Generated by Django 3.1.3 on 2020-11-23 09:36

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_auto_20201117_2123'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='ident',
            field=models.CharField(blank=True, default=uuid.uuid4, max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(max_length=1500),
        ),
    ]
