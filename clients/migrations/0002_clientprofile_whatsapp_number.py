from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientprofile',
            name='whatsapp_number',
            field=models.CharField(blank=True, help_text='Optional WhatsApp contact number, including country code or local format.', max_length=20, verbose_name='WhatsApp Number'),
        ),
    ]