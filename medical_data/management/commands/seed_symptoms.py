import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from medical_data.models import Symptom


class Command(BaseCommand):
    help = 'Seed symptoms from the medical_data backup fixture.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fixture',
            default='medical_data/fixtures/symptoms_backup.json',
            help='Path to the symptom fixture relative to the project root.',
        )

    def handle(self, *args, **options):
        fixture_path = Path(options['fixture'])
        if not fixture_path.is_absolute():
            fixture_path = settings.BASE_DIR / fixture_path

        if not fixture_path.exists():
            raise CommandError(f'Fixture not found: {fixture_path}')

        try:
            fixture_data = json.loads(fixture_path.read_text(encoding='utf-8-sig'))
        except (OSError, json.JSONDecodeError) as exc:
            raise CommandError(f'Could not read fixture: {exc}') from exc

        records = [
            record for record in fixture_data
            if record.get('model') == 'medical_data.symptom'
        ]
        if not records:
            raise CommandError('The fixture contains no medical_data.symptom records.')

        created_count = 0
        updated_count = 0

        with transaction.atomic():
            for index, record in enumerate(records, start=1):
                fields = record.get('fields', {})
                name = fields.get('name')
                if not name:
                    raise CommandError(f'Fixture record {index} has no symptom name.')

                symptom, created = Symptom.objects.update_or_create(
                    name=name,
                    defaults={
                        'description': fields.get('description', ''),
                        'is_red_flag': fields.get('is_red_flag', False),
                        'emergency_message': fields.get('emergency_message', ''),
                    },
                )

                if created:
                    created_count += 1
                else:
                    updated_count += 1

                self.stdout.write(
                    f'Seeding symptom {index}/{len(records)}: {symptom.name}...'
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully seeded {len(records)} symptoms '
                f'({created_count} created, {updated_count} updated).'
            )
        )
