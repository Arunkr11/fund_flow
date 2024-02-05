# Generated by Django 5.0.1 on 2024-01-30 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fundflowbudget', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='category',
            field=models.CharField(choices=[('fuel', 'fuel'), ('food', 'food'), ('entertainment', 'entertainment'), ('emi', 'emi'), ('bills', 'bills'), ('miscellaneous', 'miscellaneous')], max_length=225),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='type',
            field=models.CharField(choices=[('expense', 'expense'), ('income', 'income')], default='miscellaneous', max_length=225),
        ),
    ]