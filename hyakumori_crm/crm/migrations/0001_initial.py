# Generated by Django 3.0.4 on 2020-04-06 09:58

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import hyakumori_crm.crm.models.attachment
import hyakumori_crm.crm.models.customer
import hyakumori_crm.crm.models.forest
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Archive',
            fields=[
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('internal_id', models.CharField(max_length=255, null=True)),
                ('attributes', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('archive_date', models.DateField(blank=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='crm_archive_author', to=settings.AUTH_USER_MODEL)),
                ('editor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='crm_archive_editor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('store_deleted_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('internal_id', models.CharField(max_length=255, null=True)),
                ('attributes', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('contact_info', django.contrib.postgres.fields.jsonb.JSONField(default=hyakumori_crm.crm.models.customer.DefaultContact.contact_info)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='crm_contact_author', to=settings.AUTH_USER_MODEL)),
                ('editor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='crm_contact_editor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('store_deleted_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('internal_id', models.CharField(max_length=255, null=True)),
                ('attributes', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('name_kanji', django.contrib.postgres.fields.jsonb.JSONField(db_index=True, default=hyakumori_crm.crm.models.customer.DefaultCustomer.name_kanji)),
                ('name_kana', django.contrib.postgres.fields.jsonb.JSONField(db_index=True, default=hyakumori_crm.crm.models.customer.DefaultCustomer.name_kana)),
                ('address', django.contrib.postgres.fields.jsonb.JSONField(db_index=True, default=hyakumori_crm.crm.models.customer.DefaultCustomer.address)),
                ('banking', django.contrib.postgres.fields.jsonb.JSONField(default=hyakumori_crm.crm.models.customer.DefaultCustomer.banking)),
                ('tags', django.contrib.postgres.fields.jsonb.JSONField(default=list)),
                ('status', models.CharField(choices=[('registered', '登録済'), ('unregistered', '未登録')], default='unregistered', max_length=20)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='crm_customer_author', to=settings.AUTH_USER_MODEL)),
                ('editor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='crm_customer_editor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('store_deleted_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Forest',
            fields=[
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('internal_id', models.CharField(max_length=255, null=True)),
                ('attributes', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('cadastral', django.contrib.postgres.fields.jsonb.JSONField(db_index=True, default=hyakumori_crm.crm.models.forest.DefaultForest.cadastral)),
                ('owner', django.contrib.postgres.fields.jsonb.JSONField(db_index=True, default=hyakumori_crm.crm.models.forest.DefaultForest.owner)),
                ('contracts', django.contrib.postgres.fields.jsonb.JSONField(db_index=True, default=hyakumori_crm.crm.models.forest.DefaultForest.contracts)),
                ('tag', django.contrib.postgres.fields.jsonb.JSONField(default=hyakumori_crm.crm.models.forest.DefaultForest.tag)),
                ('land_attributes', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('geodata', django.contrib.postgres.fields.jsonb.JSONField(default=hyakumori_crm.crm.models.forest.DefaultForest.geodata)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='crm_forest_author', to=settings.AUTH_USER_MODEL)),
                ('editor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='crm_forest_editor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('store_deleted_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ForestCustomer',
            fields=[
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('attributes', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='crm_forestcustomer_author', to=settings.AUTH_USER_MODEL)),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='crm.Contact')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='crm.Customer')),
                ('editor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='crm_forestcustomer_editor', to=settings.AUTH_USER_MODEL)),
                ('forest', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='crm.Forest')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CustomerContact',
            fields=[
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('attributes', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='crm_customercontact_author', to=settings.AUTH_USER_MODEL)),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='crm.Contact')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='crm.Customer')),
                ('editor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='crm_customercontact_editor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('internal_id', models.CharField(max_length=255, null=True)),
                ('attributes', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('object_id', models.PositiveIntegerField()),
                ('attachment_file', models.FileField(upload_to=hyakumori_crm.crm.models.attachment.attachment_upload, verbose_name='attachment')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='crm_attachment_author', to=settings.AUTH_USER_MODEL)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='contenttypes.ContentType')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_attachments', to=settings.AUTH_USER_MODEL, verbose_name='creator')),
                ('editor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='crm_attachment_editor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'attachment',
                'verbose_name_plural': 'attachments',
                'ordering': ['-created_at'],
                'permissions': (('delete_foreign_attachments', 'Can delete foreign attachments'),),
            },
        ),
        migrations.CreateModel(
            name='ArchiveForest',
            fields=[
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('attributes', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('archive', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='crm.Archive')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='crm_archiveforest_author', to=settings.AUTH_USER_MODEL)),
                ('editor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='crm_archiveforest_editor', to=settings.AUTH_USER_MODEL)),
                ('forest', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='crm.Forest')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ArchiveCustomer',
            fields=[
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('attributes', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('archive', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='crm.Archive')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='crm_archivecustomer_author', to=settings.AUTH_USER_MODEL)),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='crm.Contact')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='crm.Customer')),
                ('editor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='crm_archivecustomer_editor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
