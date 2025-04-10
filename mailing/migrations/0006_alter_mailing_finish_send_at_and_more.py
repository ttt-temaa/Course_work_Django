import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mailing", "0005_alter_mailing_finish_send_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailing",
            name="finish_send_at",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 12, 15, 13, 55, 33, 789722),
                verbose_name="Дата и время окончания отправки",
            ),
        ),
        migrations.AlterField(
            model_name="mailing",
            name="first_send_at",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 12, 14, 13, 55, 33, 789722),
                verbose_name="Дата и время первой отправки",
            ),
        ),
    ]
