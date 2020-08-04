from django import forms
from django.contrib import admin

import simplejson

import django_prbac.csv
from django_prbac.models import *
from django_prbac.forms import StringSetInput

__all__ = [
    'RoleAdmin',
    'RoleAdminForm',
    'GrantAdmin',
]


class RoleAdminForm(forms.ModelForm):
    class Meta:
        model = Role
        widgets = {
            'parameters': StringSetInput
        }
        exclude = []


class RoleAdmin(admin.ModelAdmin):

    model = Role
    form = RoleAdminForm

    def parameters__csv(self, instance):
        return django_prbac.csv.line_to_string(sorted(list(instance.parameters)))
    parameters__csv.short_description = 'Parameters'
    parameters__csv.admin_order_field = 'parameters'

    list_display = [
        'slug',
        'name',
        'parameters__csv',
        'description',
    ]

    search_fields = [
        'slug',
        'name',
        'parameters',
        'description',
    ]


class GrantAdmin(admin.ModelAdmin):

    model = Grant

    def assignment__dumps(self, instance):
        return simplejson.dumps(instance.assignment)
    assignment__dumps.short_description = 'Assignment'

    list_display = [
        'from_role',
        'to_role',
        'assignment__dumps',
    ]

    search_fields = [
        'from_role__name',
        'from_role__description',
        'to_role__name',
        'to_role__description',
    ]

    def get_queryset(self, request):
        return Grant.objects.select_related('to_role', 'from_role')


admin.site.register(Role, RoleAdmin)
admin.site.register(Grant, GrantAdmin)
