# Generated by Django 3.0.1 on 2021-03-30 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('E_Commerce', '0002_auto_20210330_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sub_category',
            field=models.CharField(blank=True, choices=[('Mens', 'Men'), ('Womens', 'Women'), ('Kids', 'Kids')], default='', max_length=200, null=True),
        ),
    ]
