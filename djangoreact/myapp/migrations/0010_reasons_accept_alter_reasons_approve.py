# Generated by Django 4.2.7 on 2024-02-09 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_alter_reasons_notification_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='reasons',
            name='accept',
            field=models.BooleanField(default=False, help_text='Auto accept submission: Check this box if you want to automatically accept this reason upon submission. Students still have to be approved by you to have their test scheduled.'),
        ),
        migrations.AlterField(
            model_name='reasons',
            name='approve',
            field=models.BooleanField(default=False, help_text='Auto Approval: Check this box if you want to automatically approve this reason upon submission. Students will not have to be approved by you to have their test scheduled. This is not recommended for most reasons.'),
        ),
    ]
