from django.db import models
from django.db.models import UniqueConstraint


class Symptom(models.Model):
    """
    Represents a single medical symptom (e.g., Fever, Headache, Chest Pain).
    Can be flagged as a red-flag/emergency symptom.
    """
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Symptom Name',
        help_text='The common name of the symptom (e.g., Fever, Chest Pain).'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Description',
        help_text='Optional clinical description for admin reference.'
    )
    is_red_flag = models.BooleanField(
        default=False,
        verbose_name='Red Flag / Emergency Symptom',
        help_text='Check if this symptom requires immediate emergency attention.'
    )
    emergency_message = models.TextField(
        blank=True,
        verbose_name='Emergency Warning Message',
        help_text='The warning message displayed to the user if this red-flag symptom is selected.'
    )

    class Meta:
        verbose_name = 'Symptom'
        verbose_name_plural = 'Symptoms'
        ordering = ['name']

    def __str__(self):
        if self.is_red_flag:
            return f"⚠️ {self.name} (Red Flag)"
        return self.name


class Condition(models.Model):
    """
    Represents a medical condition or disease (e.g., Malaria, Influenza).
    Linked to Knowledge Base articles for informational content.
    """
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Condition Name',
        help_text='The name of the medical condition.'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Description',
        help_text='A general description of the condition.'
    )
    articles = models.ManyToManyField(
        'knowledge_base.Article',
        blank=True,
        related_name='related_conditions',
        verbose_name='Related Knowledge Base Articles',
        help_text='Select articles that provide information about this condition.'
    )

    class Meta:
        verbose_name = 'Condition'
        verbose_name_plural = 'Conditions'
        ordering = ['name']

    def __str__(self):
        return self.name


class ConditionSymptom(models.Model):
    """
    The rule-based relationship between a Condition and a Symptom.
    Stores tunable parameters like weight (importance) and whether
    the symptom is a core/defining symptom of the condition.
    """
    condition = models.ForeignKey(
        Condition,
        on_delete=models.CASCADE,
        related_name='symptom_rules',
        verbose_name='Condition'
    )
    symptom = models.ForeignKey(
        Symptom,
        on_delete=models.CASCADE,
        related_name='condition_rules',
        verbose_name='Symptom'
    )
    weight = models.PositiveIntegerField(
        default=1,
        verbose_name='Weight (Importance)',
        help_text='Higher weight means this symptom is a stronger indicator of the condition. Tunable from admin.'
    )
    is_core = models.BooleanField(
        default=False,
        verbose_name='Core Symptom',
        help_text='Check if this is a primary/defining symptom of the condition.'
    )
    notes = models.TextField(
        blank=True,
        verbose_name='Admin Notes',
        help_text='Optional notes for administrators about this rule.'
    )

    class Meta:
        verbose_name = 'Condition-Symptom Rule'
        verbose_name_plural = 'Condition-Symptom Rules'
        ordering = ['condition', '-weight', 'symptom']
        constraints = [
            UniqueConstraint(
                fields=['condition', 'symptom'],
                name='unique_condition_symptom_rule'
            )
        ]

    def __str__(self):
        core_marker = " [CORE]" if self.is_core else ""
        return f"{self.condition.name} ← {self.symptom.name} (weight: {self.weight}){core_marker}"