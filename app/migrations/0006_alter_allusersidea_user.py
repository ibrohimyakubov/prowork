# Generated by Django 3.2.5 on 2021-07-15 08:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_ideastartapper_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allusersidea',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.staff'),
        ),
    ]
