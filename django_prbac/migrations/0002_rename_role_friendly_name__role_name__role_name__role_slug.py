# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_column(u'django_prbac_role', 'name', 'slug')
        db.rename_column(u'django_prbac_role', 'friendly_name', 'name')

    def backwards(self, orm):
        db.rename_column(u'django_prbac_role', 'slug', 'name')
        db.rename_column(u'django_prbac_role', 'name', 'friendly_name')

    models = {
        u'django_prbac.grant': {
            'Meta': {'object_name': 'Grant'},
            'assignment': ('json_field.fields.JSONField', [], {'default': '{}'}),
            'from_role': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'memberships_granted'", 'to': u"orm['django_prbac.Role']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'to_role': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'members'", 'to': u"orm['django_prbac.Role']"})
        },
        u'django_prbac.role': {
            'Meta': {'object_name': 'Role'},
            'description': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'parameters': ('django_prbac.fields.StringSetField', [], {'default': '[]'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'})
        }
    }

    complete_apps = ['django_prbac']