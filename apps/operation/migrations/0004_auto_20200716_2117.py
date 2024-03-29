# Generated by Django 2.2 on 2020-07-16 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0003_auto_20200715_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfav',
            name='goods',
            field=models.ForeignKey(help_text='商品id', on_delete=django.db.models.deletion.CASCADE, to='goods.Goods', verbose_name='商品'),
        ),
        migrations.AlterField(
            model_name='userleavemessage',
            name='file',
            field=models.FileField(help_text='上传文件', upload_to='message/images/', verbose_name='上传文件'),
        ),
    ]
