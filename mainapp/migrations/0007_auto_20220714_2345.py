# Generated by Django 3.2.10 on 2022-07-14 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0006_languagespecifiedstring"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="entity",
            name="label",
        ),
        migrations.AddField(
            model_name="entity",
            name="label",
            field=models.ManyToManyField(to="mainapp.LanguageSpecifiedString"),
        ),
    ]
