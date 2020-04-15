# Generated by Django 3.0.4 on 2020-04-14 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_unfold_contact_info_20200408_0512'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='archive',
            options={'permissions': [('manage_archive', 'All permissions for archive')]},
        ),
        migrations.AlterModelOptions(
            name='archivecustomer',
            options={'permissions': [('manage_archivecustomer', 'All permissions for archive customer')]},
        ),
        migrations.AlterModelOptions(
            name='archiveforest',
            options={'permissions': [('manage_archivecustomer', 'All permissions for archive forest')]},
        ),
        migrations.AlterModelOptions(
            name='contact',
            options={'permissions': [('manage_contact', 'All permissions for contact')]},
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'permissions': [('manage_customer', 'All permissions for customer')]},
        ),
        migrations.AlterModelOptions(
            name='customercontact',
            options={'permissions': [('manage_customercontact', 'All permissions for customer contact')]},
        ),
        migrations.AlterModelOptions(
            name='forest',
            options={'permissions': [('manage_forest', 'All permissions for forest')]},
        ),
        migrations.AlterModelOptions(
            name='forestcustomer',
            options={'permissions': [('manage_forestcustomer', 'All permissions for forest customer')]},
        ),
        migrations.AlterModelManagers(
            name='archive',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='contact',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='customer',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='forest',
            managers=[
            ],
        ),
    ]
