# Generated by Django 4.1.3 on 2022-11-07 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license_plate_number', models.CharField(max_length=20, verbose_name='license plate number')),
                ('vin_code', models.CharField(max_length=17, verbose_name='vin code')),
                ('client', models.CharField(max_length=250, verbose_name='client')),
            ],
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(help_text='Enter the name of car make', max_length=200, verbose_name='make')),
                ('model', models.CharField(help_text='Enter the name of car model', max_length=200, verbose_name='model')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField(auto_now_add=True, verbose_name='order date')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=18, verbose_name='total amount')),
                ('car', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='autoservice.car')),
            ],
            options={
                'ordering': ['order_date'],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Enter the title of service', max_length=200, verbose_name='title')),
                ('price', models.DecimalField(decimal_places=2, max_digits=18, verbose_name='price')),
            ],
            options={
                'ordering': ['title', 'price'],
            },
        ),
        migrations.CreateModel(
            name='OrderLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(verbose_name='amount')),
                ('price', models.DecimalField(decimal_places=2, max_digits=18, verbose_name='price')),
                ('order', models.ManyToManyField(to='autoservice.order')),
                ('service', models.ManyToManyField(help_text='Choose service(s) for the car', to='autoservice.service', verbose_name='service(s)')),
            ],
        ),
        migrations.AddField(
            model_name='car',
            name='car_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='autoservice.carmodel'),
        ),
    ]
