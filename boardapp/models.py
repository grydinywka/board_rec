from __future__ import unicode_literals

from django.db import models

class Message(models.Model):
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    content = models.CharField(max_length=254, blank=False, null=True, default=None)
    parent = models.ForeignKey("Message", blank=True, null=True, default=None)

    def has_parent(self):
        if self.parent is not None:
            return True
        return False

    def has_comment(self):
        if self.message_set.all().count():
            return True
        return False

    def __unicode__(self):
        return u"Message #%s, time posting: %s" % (self.id, self.created)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"


from mptt.models import MPTTModel, TreeForeignKey


class Genre(MPTTModel):
    name = models.CharField(max_length=50, unique=True, null=True, default=None)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, default=None)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return u"Genre #%s, time posting: %s" % (self.name, self.created)

    class MPTTMeta:
        order_insertion_by = ['name']


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
