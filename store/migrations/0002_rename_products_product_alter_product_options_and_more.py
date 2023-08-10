# Generated by Django 4.2.4 on 2023-08-07 20:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Products',
            new_name='Product',
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-title']},
        ),
        migrations.AddField(
            model_name='collection',
            name='featured_product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='store.product'),
        ),
    ]