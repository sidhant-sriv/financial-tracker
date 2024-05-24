# Generated by Django 5.0.6 on 2024-05-24 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_category_budget'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='budget',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10, null=True),
        ),
    ]