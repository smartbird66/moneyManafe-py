# Generated by Django 3.0.7 on 2020-06-12 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addTime', models.DateTimeField(auto_now_add=True)),
                ('money', models.IntegerField()),
                ('familyAccount', models.IntegerField()),
                ('innerId', models.SmallIntegerField()),
                ('note', models.CharField(max_length=50)),
                ('consumptionType', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name': '账单',
                'verbose_name_plural': '账单',
                'db_table': 'bill',
            },
        ),
        migrations.CreateModel(
            name='borrowAndOut',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addTime', models.DateTimeField()),
                ('person', models.CharField(max_length=10)),
                ('familyAccount', models.IntegerField()),
                ('innerId', models.SmallIntegerField()),
                ('money', models.IntegerField()),
                ('deathDate', models.DateField()),
            ],
            options={
                'verbose_name': '借入借出',
                'verbose_name_plural': '借入借出',
                'db_table': 'borrowAndOut',
            },
        ),
        migrations.CreateModel(
            name='investment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addTime', models.DateTimeField(auto_now_add=True)),
                ('InvestmentType', models.CharField(max_length=6)),
                ('principal', models.IntegerField()),
                ('updateTime', models.DateTimeField(auto_now=True)),
                ('earnings', models.IntegerField()),
                ('rate', models.SmallIntegerField()),
                ('familyAccount', models.IntegerField()),
                ('innerId', models.SmallIntegerField()),
            ],
            options={
                'verbose_name': '投资理财',
                'verbose_name_plural': '投资理财',
                'db_table': 'investment',
            },
        ),
        migrations.CreateModel(
            name='member',
            fields=[
                ('name', models.CharField(max_length=10)),
                ('familyAccount', models.IntegerField()),
                ('innerId', models.SmallIntegerField()),
                ('nickName', models.CharField(max_length=15)),
                ('birthday', models.DateField()),
                ('authority', models.SmallIntegerField(default=1)),
                ('password', models.CharField(max_length=15)),
                ('account', models.IntegerField(primary_key=True, serialize=False)),
                ('addedTime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '家庭成员',
                'verbose_name_plural': '家庭成员',
                'db_table': 'member',
            },
        ),
        migrations.CreateModel(
            name='message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('familyAccount', models.IntegerField()),
                ('account', models.IntegerField()),
                ('sendTime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '消息',
                'verbose_name_plural': '消息',
                'db_table': 'message',
            },
        ),
        migrations.CreateModel(
            name='monthyBill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('billIn', models.IntegerField()),
                ('billOut', models.IntegerField()),
                ('addTime', models.DateTimeField(auto_now_add=True)),
                ('familyAccount', models.IntegerField()),
                ('innerId', models.SmallIntegerField()),
            ],
            options={
                'verbose_name': '月账单',
                'verbose_name_plural': '月账单',
                'db_table': 'monthyBill',
            },
        ),
        migrations.CreateModel(
            name='note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('account', models.IntegerField()),
                ('note', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': '便签',
                'verbose_name_plural': '便签',
                'db_table': 'note',
            },
        ),
        migrations.AlterField(
            model_name='superman',
            name='password',
            field=models.CharField(max_length=15),
        ),
    ]
