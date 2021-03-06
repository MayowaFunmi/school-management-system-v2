# Generated by Django 4.0.4 on 2022-04-23 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0002_alter_nonteachingstaff_religion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='religion',
            field=models.CharField(choices=[('Christianity', 'Christianity'), ('Islam', 'Islam'), ('Others', 'Others')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='teachingstaff',
            name='religion',
            field=models.CharField(choices=[('Christianity', 'Christianity'), ('Islam', 'Islam'), ('Others', 'Others')], max_length=20, null=True),
        ),
    ]
