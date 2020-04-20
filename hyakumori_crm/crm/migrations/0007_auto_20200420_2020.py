# Generated by Django 3.0.4 on 2020-04-20 20:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0006_drop_author_editor_20200415_0616'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='archive',
            options={'permissions': [('manage_archive', 'All permissions for archive')]},
        ),
        migrations.AlterModelOptions(
            name='archivecustomer',
            options={},
        ),
        migrations.RemoveField(
            model_name='forestcustomer',
            name='contact',
        ),
        migrations.AddField(
            model_name='customercontact',
            name='forestcustomer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='crm.ForestCustomer'),
        ),
        migrations.AlterField(
            model_name='customercontact',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='crm.Contact'),
        ),
        migrations.AlterField(
            model_name='customercontact',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Customer'),
        ),
        migrations.AlterField(
            model_name='forestcustomer',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Customer'),
        ),
        migrations.AlterField(
            model_name='forestcustomer',
            name='forest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='crm.Forest'),
        ),
    ]
