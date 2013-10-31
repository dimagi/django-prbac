# Use modern Python
from __future__ import unicode_literals, absolute_import, print_function

# Django imports
from django.contrib import admin
from django import forms
from django.core import urlresolvers

# External librariess
import simplejson

# Local imports
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


class RoleAdmin(admin.ModelAdmin):

    model = Role
    form = RoleAdminForm

    def parameters__csv(self, instance):
        return django_prbac.csv.line_to_string(sorted(list(instance.parameters)))
    parameters__csv.short_description = 'Parameters'
    parameters__csv.admin_order_field = 'parameters'

    list_display = [
        'name',
        'friendly_name',
        'parameters__csv',
        'description',
    ]

    search_fields = [
        'name',
        'friendly_name',
        'parameters',
        'description',
    ]

class GrantAdmin(admin.ModelAdmin):

    model = Grant

    def edit_link(self, instance):
        if instance.id:
            return '<a href="%s">(edit)</a>' % urlresolvers.reverse('admin:django_prbac_grant_change',
                                                                         args=[instance.id])
        else:
            return ''
    edit_link.allow_tags = True
    edit_link.short_description = ''

    def assignment__dumps(self, instance):
        return simplejson.dumps(instance.assignment)
    assignment__dumps.short_description = 'Assignment'

    list_display = [
        'edit_link',
        'from_role',
        'to_role',
        'assignment__dumps',
    ]

    search_fields = [
        'from_role__name',
        'from_role__friendly_name',
        'from_role__description',
        'to_role__name',
        'to_role__friendly_name',
        'to_role__description',
    ]

    def queryset(self, request):
        return Grant.objects.select_related('to_role', 'from_role')

admin.site.register(Role, RoleAdmin)
admin.site.register(Grant, GrantAdmin)

