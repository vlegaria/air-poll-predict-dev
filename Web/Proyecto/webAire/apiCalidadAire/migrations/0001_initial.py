# Generated by Django 5.1 on 2024-09-05 22:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contaminantes',
            fields=[
                ('idContaminante', models.AutoField(primary_key=True, serialize=False)),
                ('Contaminante', models.CharField(default='', max_length=50)),
                ('descContaminante', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='estacionesCAME',
            fields=[
                ('idEstacion', models.AutoField(primary_key=True, serialize=False)),
                ('key', models.CharField(max_length=5)),
                ('name', models.CharField(max_length=100)),
                ('ID', models.CharField(max_length=50)),
                ('O3', models.IntegerField(default='0')),
                ('CO', models.IntegerField(default='0')),
                ('SO2', models.IntegerField(default='0')),
                ('NO2', models.IntegerField(default='0')),
                ('PM10', models.IntegerField(default='0')),
                ('PM25', models.IntegerField(default='0')),
                ('status', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('municipality', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('altitude', models.CharField(max_length=100)),
                ('latitude', models.CharField(max_length=100)),
                ('longitude', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=500)),
                ('website', models.CharField(max_length=200)),
                ('notes', models.CharField(max_length=300)),
                ('traffic', models.CharField(max_length=5)),
                ('xTileIn', models.CharField(max_length=50)),
                ('yTileIn', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='EstatusCalidad',
            fields=[
                ('idEstatus', models.AutoField(primary_key=True, serialize=False)),
                ('descEstatus', models.CharField(max_length=50)),
                ('recomendacion', models.CharField(max_length=100)),
                ('descColor', models.CharField(max_length=50)),
                ('valorColor', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='MER_15M',
            fields=[
                ('idData', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('CO', models.DecimalField(decimal_places=6, max_digits=16)),
                ('NO', models.DecimalField(decimal_places=6, max_digits=16)),
                ('NOX', models.DecimalField(decimal_places=6, max_digits=16)),
                ('NO2', models.DecimalField(decimal_places=6, max_digits=16)),
                ('O3', models.DecimalField(decimal_places=6, max_digits=16)),
                ('PM10', models.DecimalField(decimal_places=6, max_digits=16)),
                ('PM25', models.DecimalField(decimal_places=6, max_digits=16)),
                ('RH', models.DecimalField(decimal_places=6, max_digits=16)),
                ('SO2', models.DecimalField(decimal_places=6, max_digits=16)),
                ('TMP', models.DecimalField(decimal_places=6, max_digits=16)),
                ('WDR', models.DecimalField(decimal_places=6, max_digits=16)),
                ('WSP', models.DecimalField(decimal_places=6, max_digits=16)),
                ('year', models.IntegerField()),
                ('month', models.IntegerField(default='0')),
                ('day', models.IntegerField(default='0')),
                ('hour', models.IntegerField()),
                ('minutes', models.IntegerField()),
                ('traffic', models.DecimalField(decimal_places=6, default='0.00', max_digits=16)),
            ],
        ),
        migrations.CreateModel(
            name='MER_NORM',
            fields=[
                ('idData', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('CO', models.DecimalField(decimal_places=12, max_digits=13)),
                ('NO', models.DecimalField(decimal_places=12, max_digits=13)),
                ('NOX', models.DecimalField(decimal_places=12, max_digits=13)),
                ('NO2', models.DecimalField(decimal_places=12, max_digits=13)),
                ('O3', models.DecimalField(decimal_places=12, max_digits=13)),
                ('PM10', models.DecimalField(decimal_places=12, max_digits=13)),
                ('PM25', models.DecimalField(decimal_places=12, max_digits=13)),
                ('RH', models.DecimalField(decimal_places=12, max_digits=13)),
                ('SO2', models.DecimalField(decimal_places=12, max_digits=13)),
                ('TMP', models.DecimalField(decimal_places=12, max_digits=13)),
                ('WDR', models.DecimalField(decimal_places=12, max_digits=13)),
                ('WSP', models.DecimalField(decimal_places=12, max_digits=13)),
                ('year', models.IntegerField()),
                ('month', models.IntegerField(default='0')),
                ('day', models.IntegerField()),
                ('hour', models.IntegerField()),
                ('minutes', models.IntegerField()),
                ('traffic', models.DecimalField(decimal_places=12, default='0.00', max_digits=13)),
            ],
        ),
        migrations.CreateModel(
            name='MER_PROM_HR',
            fields=[
                ('idData', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('CO', models.DecimalField(decimal_places=6, max_digits=16)),
                ('NO', models.DecimalField(decimal_places=6, max_digits=16)),
                ('NOX', models.DecimalField(decimal_places=6, max_digits=16)),
                ('NO2', models.DecimalField(decimal_places=6, max_digits=16)),
                ('O3', models.DecimalField(decimal_places=6, max_digits=16)),
                ('PM10', models.DecimalField(decimal_places=6, max_digits=16)),
                ('PM25', models.DecimalField(decimal_places=6, max_digits=16)),
                ('RH', models.DecimalField(decimal_places=6, max_digits=16)),
                ('SO2', models.DecimalField(decimal_places=6, max_digits=16)),
                ('TMP', models.DecimalField(decimal_places=6, max_digits=16)),
                ('WDR', models.DecimalField(decimal_places=6, max_digits=16)),
                ('WSP', models.DecimalField(decimal_places=6, max_digits=16)),
                ('year', models.IntegerField()),
                ('month', models.IntegerField(default='0')),
                ('day', models.IntegerField()),
                ('hour', models.IntegerField()),
                ('minutes', models.IntegerField()),
                ('traffic', models.DecimalField(decimal_places=6, default='0.00', max_digits=16)),
            ],
        ),
        migrations.CreateModel(
            name='PED_15M',
            fields=[
                ('idData', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('CO', models.DecimalField(decimal_places=6, max_digits=16)),
                ('NO', models.DecimalField(decimal_places=6, max_digits=16)),
                ('NOX', models.DecimalField(decimal_places=6, max_digits=16)),
                ('NO2', models.DecimalField(decimal_places=6, max_digits=16)),
                ('O3', models.DecimalField(decimal_places=6, max_digits=16)),
                ('PM10', models.DecimalField(decimal_places=6, max_digits=16)),
                ('PM25', models.DecimalField(decimal_places=6, max_digits=16)),
                ('RH', models.DecimalField(decimal_places=6, max_digits=16)),
                ('SO2', models.DecimalField(decimal_places=6, max_digits=16)),
                ('TMP', models.DecimalField(decimal_places=6, max_digits=16)),
                ('WDR', models.DecimalField(decimal_places=6, max_digits=16)),
                ('WSP', models.DecimalField(decimal_places=6, max_digits=16)),
                ('year', models.IntegerField()),
                ('month', models.IntegerField(default='0')),
                ('day', models.IntegerField()),
                ('hour', models.IntegerField()),
                ('minutes', models.IntegerField()),
                ('traffic', models.DecimalField(decimal_places=6, default='0.00', max_digits=16)),
            ],
        ),
        migrations.CreateModel(
            name='PED_NORM',
            fields=[
                ('idData', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('CO', models.DecimalField(decimal_places=12, max_digits=13)),
                ('NO', models.DecimalField(decimal_places=12, max_digits=13)),
                ('NOX', models.DecimalField(decimal_places=12, max_digits=13)),
                ('NO2', models.DecimalField(decimal_places=12, max_digits=13)),
                ('O3', models.DecimalField(decimal_places=12, max_digits=13)),
                ('PM10', models.DecimalField(decimal_places=12, max_digits=13)),
                ('PM25', models.DecimalField(decimal_places=12, max_digits=13)),
                ('RH', models.DecimalField(decimal_places=12, max_digits=13)),
                ('SO2', models.DecimalField(decimal_places=12, max_digits=13)),
                ('TMP', models.DecimalField(decimal_places=12, max_digits=13)),
                ('WDR', models.DecimalField(decimal_places=12, max_digits=13)),
                ('WSP', models.DecimalField(decimal_places=12, max_digits=13)),
                ('year', models.IntegerField()),
                ('month', models.IntegerField(default='0')),
                ('day', models.IntegerField()),
                ('hour', models.IntegerField()),
                ('minutes', models.IntegerField()),
                ('traffic', models.DecimalField(decimal_places=12, default='0.00', max_digits=13)),
            ],
        ),
        migrations.CreateModel(
            name='PED_PROM_HR',
            fields=[
                ('idData', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('CO', models.DecimalField(decimal_places=6, max_digits=16)),
                ('NO', models.DecimalField(decimal_places=6, max_digits=16)),
                ('NOX', models.DecimalField(decimal_places=6, max_digits=16)),
                ('NO2', models.DecimalField(decimal_places=6, max_digits=16)),
                ('O3', models.DecimalField(decimal_places=6, max_digits=16)),
                ('PM10', models.DecimalField(decimal_places=6, max_digits=16)),
                ('PM25', models.DecimalField(decimal_places=6, max_digits=16)),
                ('RH', models.DecimalField(decimal_places=6, max_digits=16)),
                ('SO2', models.DecimalField(decimal_places=6, max_digits=16)),
                ('TMP', models.DecimalField(decimal_places=6, max_digits=16)),
                ('WDR', models.DecimalField(decimal_places=6, max_digits=16)),
                ('WSP', models.DecimalField(decimal_places=6, max_digits=16)),
                ('year', models.IntegerField()),
                ('month', models.IntegerField(default='0')),
                ('day', models.IntegerField()),
                ('hour', models.IntegerField()),
                ('minutes', models.IntegerField()),
                ('traffic', models.DecimalField(decimal_places=6, default='0.00', max_digits=16)),
            ],
        ),
        migrations.CreateModel(
            name='UIZ_15M',
            fields=[
                ('idData', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('CO', models.DecimalField(decimal_places=6, max_digits=16)),
                ('NO', models.DecimalField(decimal_places=6, max_digits=16)),
                ('NOX', models.DecimalField(decimal_places=6, max_digits=16)),
                ('NO2', models.DecimalField(decimal_places=6, max_digits=16)),
                ('O3', models.DecimalField(decimal_places=6, max_digits=16)),
                ('PM10', models.DecimalField(decimal_places=6, max_digits=16)),
                ('PM25', models.DecimalField(decimal_places=6, max_digits=16)),
                ('RH', models.DecimalField(decimal_places=6, max_digits=16)),
                ('SO2', models.DecimalField(decimal_places=6, max_digits=16)),
                ('TMP', models.DecimalField(decimal_places=6, max_digits=16)),
                ('WDR', models.DecimalField(decimal_places=6, max_digits=16)),
                ('WSP', models.DecimalField(decimal_places=6, max_digits=16)),
                ('year', models.IntegerField()),
                ('month', models.IntegerField(default='0')),
                ('day', models.IntegerField()),
                ('hour', models.IntegerField()),
                ('minutes', models.IntegerField()),
                ('traffic', models.DecimalField(decimal_places=6, default='0.00', max_digits=16)),
            ],
        ),
        migrations.CreateModel(
            name='UIZ_NORM',
            fields=[
                ('idData', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('CO', models.DecimalField(decimal_places=12, max_digits=13)),
                ('NO', models.DecimalField(decimal_places=12, max_digits=13)),
                ('NOX', models.DecimalField(decimal_places=12, max_digits=13)),
                ('NO2', models.DecimalField(decimal_places=12, max_digits=13)),
                ('O3', models.DecimalField(decimal_places=12, max_digits=13)),
                ('PM10', models.DecimalField(decimal_places=12, max_digits=13)),
                ('PM25', models.DecimalField(decimal_places=12, max_digits=13)),
                ('RH', models.DecimalField(decimal_places=12, max_digits=13)),
                ('SO2', models.DecimalField(decimal_places=12, max_digits=13)),
                ('TMP', models.DecimalField(decimal_places=12, max_digits=13)),
                ('WDR', models.DecimalField(decimal_places=12, max_digits=13)),
                ('WSP', models.DecimalField(decimal_places=12, max_digits=13)),
                ('year', models.IntegerField()),
                ('month', models.IntegerField(default='0')),
                ('day', models.IntegerField()),
                ('hour', models.IntegerField()),
                ('minutes', models.IntegerField()),
                ('traffic', models.DecimalField(decimal_places=12, default='0.00', max_digits=13)),
            ],
        ),
        migrations.CreateModel(
            name='UIZ_PROM_HR',
            fields=[
                ('idData', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('CO', models.DecimalField(decimal_places=6, max_digits=16)),
                ('NO', models.DecimalField(decimal_places=6, max_digits=16)),
                ('NOX', models.DecimalField(decimal_places=6, max_digits=16)),
                ('NO2', models.DecimalField(decimal_places=6, max_digits=16)),
                ('O3', models.DecimalField(decimal_places=6, max_digits=16)),
                ('PM10', models.DecimalField(decimal_places=6, max_digits=16)),
                ('PM25', models.DecimalField(decimal_places=6, max_digits=16)),
                ('RH', models.DecimalField(decimal_places=6, max_digits=16)),
                ('SO2', models.DecimalField(decimal_places=6, max_digits=16)),
                ('TMP', models.DecimalField(decimal_places=6, max_digits=16)),
                ('WDR', models.DecimalField(decimal_places=6, max_digits=16)),
                ('WSP', models.DecimalField(decimal_places=6, max_digits=16)),
                ('year', models.IntegerField()),
                ('month', models.IntegerField(default='0')),
                ('day', models.IntegerField()),
                ('hour', models.IntegerField()),
                ('minutes', models.IntegerField()),
                ('traffic', models.DecimalField(decimal_places=6, default='0.00', max_digits=16)),
            ],
        ),
        migrations.CreateModel(
            name='Unidades',
            fields=[
                ('idUnidad', models.AutoField(primary_key=True, serialize=False)),
                ('descUnidad', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Prediccion',
            fields=[
                ('idPrediccion', models.AutoField(primary_key=True, serialize=False)),
                ('valorContaminante', models.DecimalField(decimal_places=4, max_digits=6)),
                ('fechaPrediccion', models.DateTimeField(auto_now_add=True)),
                ('Contaminante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apicalidadaire.contaminantes')),
                ('Estacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apicalidadaire.estacionescame')),
                ('Estatus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apicalidadaire.estatuscalidad')),
                ('Unidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apicalidadaire.unidades')),
            ],
        ),
    ]
