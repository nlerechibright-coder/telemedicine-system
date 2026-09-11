from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('episodes', '0002_doctorrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='healthepisode',
            name='video_started_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Video Consultation Started At'),
        ),
    ]