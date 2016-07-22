from __future__ import unicode_literals

from django.db import models

from mptt.models import MPTTModel, TreeForeignKey

class BaseNotice(MPTTModel):
    """Base class for Messages and Comments"""
    content = models.TextField(blank=False, null=True, default=None)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, default=None)

    class Meta:
        abstract = True


class Notice(BaseNotice):
    """class for root messages (in top of tree)"""

    user = models.ForeignKey('auth.User', null=True, blank=False, default=None)
    def save(self, *args, **kwargs):
        if self.parent is not None:
            try:
                self.insert_at(self.parent, position='last-child', save=False)
            except ValueError:
                self.move_to(self.parent, position='last-child')
        super(Notice, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"Notice #%s, time posting: %s" % (self.id, self.created)

    class MPTTMeta:
        order_insertion_by = ['-created']
