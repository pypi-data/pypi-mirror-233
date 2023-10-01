from django.db import models
from django.conf import settings as settings_raw

settings = settings_raw.__dict__
settings['APPS'] = ['main']
if getattr(settings_raw, 'DRF_REACT_BY_SCHEMA', None):
    settings['APPS'] = settings_raw.DRF_REACT_BY_SCHEMA.get('APPS', ['main'])

class ForeignKey(models.ForeignKey):
    description = "Extended ForeignKey"

    def __init__(self, *args, related_editable=True, label='', **kwargs):
        super().__init__(*args, **kwargs)
        self.related_editable = related_editable
        self.label = label


class ManyToManyField(models.ManyToManyField):
    description = "Extended Many to Many Field"

    def __init__(self, *args, related_editable=True, label='', **kwargs):
        super().__init__(*args, **kwargs)
        self.related_editable = related_editable
        self.label = label


class OneToOneField(models.OneToOneField):
    description = "Extended One to One Field"

    def __init__(self, *args, related_editable=True, label='', **kwargs):
        super().__init__(*args, **kwargs)
        self.related_editable = related_editable
        self.label = label


class DecimalField(models.DecimalField):
    description = "Extended DecimalField"

    def __init__(self, *args, is_currency=True, prefix='', suffix='', **kwargs):
        super().__init__(*args, **kwargs)
        self.is_currency = is_currency and prefix == '' and suffix == ''
        self.prefix = prefix
        self.suffix = suffix


class DateField(models.DateField):
    description = "Extended DateField"

    def __init__(self, *args, views=None, **kwargs):
        super().__init__(*args, **kwargs)
        if views:
            self.views = views
