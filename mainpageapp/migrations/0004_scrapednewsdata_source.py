# Generated by Django 5.0.6 on 2024-06-17 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpageapp', '0003_alter_scrapednewsdata_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='scrapednewsdata',
            name='source',
            field=models.CharField(max_length=40, null=True),
        ),
    ]
