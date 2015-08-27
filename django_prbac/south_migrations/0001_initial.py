# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Role'
        db.create_table(u'django_prbac_role', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256)),
            ('friendly_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('description', self.gf('django.db.models.fields.TextField')(default=u'')),
            ('parameters', self.gf('django_prbac.fields.StringSetField')(default=[])),
        ))
        db.send_create_signal(u'django_prbac', ['Role'])

        # Adding model 'Grant'
        db.create_table(u'django_prbac_grant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_role', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'memberships_granted', to=orm['django_prbac.Role'])),
            ('to_role', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'members', to=orm['django_prbac.Role'])),
            ('assignment', self.gf('json_field.fields.JSONField')(default={})),
        ))
        db.send_create_signal(u'django_prbac', ['Grant'])


    def backwards(self, orm):
        # Deleting model 'Role'
        db.delete_table(u'django_prbac_role')

        # Deleting model 'Grant'
        db.delete_table(u'django_prbac_grant')


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
            'description': ('django.db.models.fields.TextField', [], {'default': "u''"}),
            'friendly_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'parameters': ('django_prbac.fields.StringSetField', [], {'default': '[]'})
        }
    }

    complete_apps = ['django_prbac']