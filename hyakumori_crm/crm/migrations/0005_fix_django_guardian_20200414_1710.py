# Generated by Django 3.0.4 on 2020-04-14 17:10

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('crm', '0004_permissions_20200414_0952'),
    ]

    operations = [
        migrations.RunSQL(
            sql=["alter table guardian_userobjectpermission alter column object_pk type uuid using object_pk::uuid;"],
            reverse_sql=[
                "alter table guardian_userobjectpermission alter column object_pk type varchar using object_pk::varchar"]
        ),
        migrations.RunSQL(
            sql=["alter table guardian_groupobjectpermission alter column object_pk type uuid using object_pk::uuid;"],
            reverse_sql=[
                "alter table guardian_groupobjectpermission alter column object_pk type varchar using object_pk::varchar"]
        ),
    ]
