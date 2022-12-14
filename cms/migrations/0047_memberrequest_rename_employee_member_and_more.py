# Generated by Django 4.0.4 on 2022-07-12 16:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cms', '0046_task_author_alter_employeerequest_requested_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40)),
                ('description', models.TextField(max_length=300)),
                ('requested_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_resolved', models.BooleanField(default=False)),
                ('from_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Sentfrom+', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name=' Sentto+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RenameModel(
            old_name='Employee',
            new_name='Member',
        ),
        migrations.RemoveField(
            model_name='task',
            name='employee',
        ),
        migrations.AddField(
            model_name='task',
            name='member',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='member+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='project',
            name='date_added',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.DeleteModel(
            name='EmployeeRequest',
        ),
    ]
