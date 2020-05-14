# Generated by Django 3.0.4 on 2020-05-02 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0010_rename_forest_tag_20200502_1115'),
    ]

    operations = [
        migrations.RunSQL(
            sql=[
                """
                    update crm_forest
                    set tags = tags - 'danchi' || jsonb_build_object('団地', tags->'danchi')
                    where tags ? 'danchi'
                """,
                """
                     update crm_forest
                     set tags = tags - 'manage_type' || jsonb_build_object('管理形態', tags->'manage_type')
                     where tags ? 'manage_type'
                 """
            ],
        ),
    ]
