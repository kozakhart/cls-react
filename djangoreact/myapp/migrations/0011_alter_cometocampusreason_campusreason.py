# Generated by Django 4.2.7 on 2024-02-16 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_reasons_accept_alter_reasons_approve'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cometocampusreason',
            name='campusreason',
            field=models.CharField(default='None', max_length=100),
        ),
    ]
