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

