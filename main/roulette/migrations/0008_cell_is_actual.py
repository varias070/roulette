# Generated by Django 4.2.5 on 2023-09-10 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roulette', '0007_rename_cells_cell_game'),
    ]

    operations = [
        migrations.AddField(
            model_name='cell',
            name='is_actual',
            field=models.BooleanField(default=True),
        ),
    ]
