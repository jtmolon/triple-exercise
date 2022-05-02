# Generated by Django 4.0.3 on 2022-05-02 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0001_initial'),
        ('banks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bank',
            name='countries',
        ),
        migrations.AddField(
            model_name='bank',
            name='countries',
            field=models.ManyToManyField(related_name='banks', to='general.country'),
        ),
    ]
