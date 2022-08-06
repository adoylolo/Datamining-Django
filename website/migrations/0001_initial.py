# Generated by Django 4.0.2 on 2022-02-25 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='data',
            fields=[
                ('invoice', models.PositiveIntegerField(primary_key=True, serialize=False, verbose_name='NO. INVOICE')),
                ('almond', models.BooleanField(default=False, verbose_name='Almond')),
                ('alpukat', models.BooleanField(default=False, verbose_name='Alpukat')),
                ('anggur', models.BooleanField(default=False, verbose_name='Anggur')),
                ('apel', models.BooleanField(default=False, verbose_name='Apel')),
                ('asam_bangkok', models.BooleanField(default=False, verbose_name='Asam Bangkok')),
                ('avomango', models.BooleanField(default=False, verbose_name='Avomango')),
                ('blueberry_arg', models.BooleanField(default=False, verbose_name='Blueberry Argentina')),
                ('buah_naga', models.BooleanField(default=False, verbose_name='Buah Naga')),
                ('buah_tin', models.BooleanField(default=False, verbose_name='Buah Tin')),
                ('cherry_aus', models.BooleanField(default=False, verbose_name='Cherry Australia')),
                ('chia_seed', models.BooleanField(default=False, verbose_name='Chia Seed')),
                ('delima', models.BooleanField(default=False, verbose_name='Delima')),
                ('durian', models.BooleanField(default=False, verbose_name='Durian Monthong Frozen')),
                ('grapeola', models.BooleanField(default=False, verbose_name='GrapeOla')),
                ('jambu_kristal', models.BooleanField(default=False, verbose_name='Jambu Kristal')),
                ('jeruk', models.BooleanField(default=False, verbose_name='Jeruk')),
                ('kiwi', models.BooleanField(default=False, verbose_name='Kiwi')),
                ('kurma', models.BooleanField(default=False, verbose_name='Kurma')),
                ('lemon', models.BooleanField(default=False, verbose_name='Lemon')),
                ('lengkeng', models.BooleanField(default=False, verbose_name='Lengkeng Bangkok')),
                ('mangga', models.BooleanField(default=False, verbose_name='Mangga')),
                ('melon_golden', models.BooleanField(default=False, verbose_name='Melon Golden')),
                ('nanas_honi', models.BooleanField(default=False, verbose_name='Nanas Honi')),
                ('nectarin_aus', models.BooleanField(default=False, verbose_name='Nectarin Australia')),
                ('peach_aus', models.BooleanField(default=False, verbose_name='Peach Australia')),
                ('pear', models.BooleanField(default=False, verbose_name='Pear')),
                ('pisang', models.BooleanField(default=False, verbose_name='Pisang Cavendisk')),
                ('plum', models.BooleanField(default=False, verbose_name='Plum')),
                ('salak_pondoh', models.BooleanField(default=False, verbose_name='Salak Pondoh')),
            ],
        ),
    ]
