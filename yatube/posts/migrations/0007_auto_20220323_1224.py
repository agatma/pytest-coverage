# Generated by Django 2.2.16 on 2022-03-23 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_auto_20220323_1033'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='follow',
            options={'ordering': ('-author',)},
        ),
    ]