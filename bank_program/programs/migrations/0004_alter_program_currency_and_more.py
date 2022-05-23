# Generated by Django 4.0.3 on 2022-05-02 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0001_initial'),
        ('programs', '0003_remove_programeligibility_currency_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.currency'),
        ),
        migrations.AlterField(
            model_name='programeligibility',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.country'),
        ),
        migrations.AlterField(
            model_name='programeligibility',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eligible_for', to='programs.program'),
        ),
    ]
