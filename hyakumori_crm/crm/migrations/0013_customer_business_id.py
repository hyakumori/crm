# Generated by Django 3.0.4 on 2020-05-20 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0012_archive_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='business_id',
            field=models.CharField(db_index=True, default='', max_length=255),
        ),
    ]
