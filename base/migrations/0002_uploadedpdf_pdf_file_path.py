# Generated by Django 4.2.4 on 2023-08-08 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedpdf',
            name='pdf_file_path',
            field=models.FilePathField(null=True),
        ),
    ]
