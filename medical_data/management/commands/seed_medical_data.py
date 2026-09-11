"""
Management command to seed the medical_data database with initial data.

Usage:
    python manage.py seed_medical_data

This command is idempotent - running it multiple times will not create
duplicate records. Existing records will be updated with new values if
the seed data has changed.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from medical_data.models import Symptom, Condition, ConditionSymptom
from knowledge_base.models import Article
from medical_data import seed_data


class Command(BaseCommand):
    help = 'Seed the medical_data database with initial symptoms, conditions, and rules.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all existing medical data before seeding.',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing medical data...'))
            ConditionSymptom.objects.all().delete()
            Condition.objects.all().delete()
            Symptom.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared.'))

        self.stdout.write('Starting medical data seeding...')

        with transaction.atomic():
            symptoms_created, symptoms_updated = self._seed_symptoms()
            conditions_created, conditions_updated = self._seed_conditions()
            rules_created, rules_updated = self._seed_condition_symptom_rules()

        self.stdout.write(self.style.SUCCESS(
            f'\nSeeding complete!\n'
            f'  Symptoms:    {symptoms_created} created, {symptoms_updated} updated\n'
            f'  Conditions:  {conditions_created} created, {conditions_updated} updated\n'
            f'  Rules:       {rules_created} created, {rules_updated} updated'
        ))

    def _seed_symptoms(self):
        """Seed all symptoms from seed_data.SYMPTOMS."""
        created_count = 0
        updated_count = 0

        self.stdout.write(f'\nSeeding {len(seed_data.SYMPTOMS)} symptoms...')

        for symptom_data in seed_data.SYMPTOMS:
            # Validate red-flag symptoms have an emergency message
            if symptom_data.get('is_red_flag') and not symptom_data.get('emergency_message'):
                self.stdout.write(self.style.WARNING(
                    f"  WARNING: Red-flag symptom '{symptom_data['name']}' has no emergency_message. Skipping."
                ))
                continue

            _, created = Symptom.objects.update_or_create(
                name=symptom_data['name'],
                defaults={
                    'description': symptom_data.get('description', ''),
                    'is_red_flag': symptom_data.get('is_red_flag', False),
                    'emergency_message': symptom_data.get('emergency_message', ''),
                }
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(f'  Symptoms processed: {created_count} created, {updated_count} updated')
        return created_count, updated_count

    def _seed_conditions(self):
        """Seed all conditions from seed_data.CONDITIONS and link to KB articles."""
        created_count = 0
        updated_count = 0

        self.stdout.write(f'\nSeeding {len(seed_data.CONDITIONS)} conditions...')

        for condition_data in seed_data.CONDITIONS:
            condition, created = Condition.objects.update_or_create(
                name=condition_data['name'],
                defaults={
                    'description': condition_data.get('description', ''),
                }
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

            # Try to link to existing Knowledge Base articles by title
            article_titles = condition_data.get('article_titles', [])
            if article_titles:
                linked_count = 0
                for title in article_titles:
                    try:
                        article = Article.objects.get(title=title, is_published=True)
                        condition.articles.add(article)
                        linked_count += 1
                    except Article.DoesNotExist:
                        # Article doesn't exist yet - skip silently
                        pass
                    except Article.MultipleObjectsReturned:
                        # Multiple articles with same title - take the first published one
                        article = Article.objects.filter(title=title, is_published=True).first()
                        if article:
                            condition.articles.add(article)
                            linked_count += 1

                if linked_count > 0:
                    self.stdout.write(f'  Linked {linked_count} KB article(s) to condition: {condition.name}')

        self.stdout.write(f'  Conditions processed: {created_count} created, {updated_count} updated')
        return created_count, updated_count

    def _seed_condition_symptom_rules(self):
        """Seed all condition-symptom rules from seed_data.CONDITION_SYMPTOM_RULES."""
        created_count = 0
        updated_count = 0
        skipped_count = 0

        self.stdout.write(f'\nSeeding {len(seed_data.CONDITION_SYMPTOM_RULES)} condition-symptom rules...')

        for rule_data in seed_data.CONDITION_SYMPTOM_RULES:
            try:
                condition = Condition.objects.get(name=rule_data['condition_name'])
                symptom = Symptom.objects.get(name=rule_data['symptom_name'])
            except Condition.DoesNotExist:
                self.stdout.write(self.style.WARNING(
                    f"  WARNING: Condition '{rule_data['condition_name']}' not found. Skipping rule."
                ))
                skipped_count += 1
                continue
            except Symptom.DoesNotExist:
                self.stdout.write(self.style.WARNING(
                    f"  WARNING: Symptom '{rule_data['symptom_name']}' not found. Skipping rule."
                ))
                skipped_count += 1
                continue

            _, created = ConditionSymptom.objects.update_or_create(
                condition=condition,
                symptom=symptom,
                defaults={
                    'weight': rule_data.get('weight', 1),
                    'is_core': rule_data.get('is_core', False),
                    'notes': rule_data.get('notes', ''),
                }
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            f'  Rules processed: {created_count} created, {updated_count} updated, {skipped_count} skipped'
        )
        return created_count, updated_count