from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_task_owner_task_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='owner',
            new_name='user',
        ),
    ]
