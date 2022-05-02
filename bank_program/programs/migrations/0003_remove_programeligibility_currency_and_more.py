# Generated by Django 4.0.3 on 2022-05-02 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0002_programeligibility'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='programeligibility',
            name='currency',
        ),
        migrations.AlterField(
            model_name='programeligibility',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programs.program'),
        ),
    ]
