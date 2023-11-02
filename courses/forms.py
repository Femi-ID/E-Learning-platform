from django import forms
from django.forms.models import inlineformset_factory
from .models import Course, Module

"""Formsets- an abstraction layer to work with multiple forms on the same page"""
ModuleFormset = inlineformset_factory(Course,
                                      Module,
                                      fields=['title', 'description'],
                                      extra=2,
                                      can_delete=True)

# This function allows you to build a model formset dynamically for the Module objects related to a Course object.
# You can learn more about formsets at: https://docs.djangoproject.com/en/3.0/topics/forms/formsets/
# and about model formsets at: https://docs.djangoproject.com/en/3.0/topics/forms/modelforms/#model-formsets.

