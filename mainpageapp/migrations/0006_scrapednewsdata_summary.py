# Generated by Django 5.0.7 on 2024-08-12 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpageapp', '0005_states'),
    ]

    operations = [
        migrations.AddField(
            model_name='scrapednewsdata',
            name='summary',
            field=models.TextField(blank=True, null=True),
        ),
    ]
