# Generated by Django 3.1.2 on 2020-11-15 19:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('studentHelper', '0003_auto_20201114_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='period_type',
            field=models.CharField(choices=[('ONCE', 'Once'), ('DAILY', 'Daily'), ('WEEKLY', 'Weekly'), ('MONTHLY', 'Monthly'), ('YEARLY', 'Yearly'), ('EVEN', 'Even'), ('ODD', 'Odd')], max_length=7),
        ),
        migrations.CreateModel(
            name='Marks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('mark_type', models.CharField(choices=[('PLUS', '+'), ('MINUS', '-'), ('PKT', 'pkt'), ('MARK', 'mark')], max_length=7)),
                ('course_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='studentHelper.course')),
            ],
        ),
    ]