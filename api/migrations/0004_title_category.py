# Generated by Django 3.0.5 on 2020-12-11 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20201211_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category', to='api.Category'),
        ),
    ]
