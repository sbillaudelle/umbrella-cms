from django.db import models

class Language(models.Model):

    name = models.CharField(max_length=50)
    code = models.CharField(max_length=8)

    def __unicode__(self):
        return u"{0}".format(self.name)


class Page(models.Model):

    title = models.CharField(max_length=200)
    content = models.TextField()

    last_update = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"{0}".format(self.title)


class PageTranslation(models.Model):

    title = models.CharField(max_length=200)
    content = models.TextField()
    language = models.ForeignKey(Language, related_name='page_translations')

    page = models.ForeignKey(Page, related_name='translations')

    def __unicode__(self):
        return u"{0}".format(self.title)


class Location(models.Model):

    location = models.CharField(max_length=200)
    page = models.ForeignKey(Page, related_name='locations')

    def __unicode__(self):
        return u"{0}".format(self.location)


class Link(models.Model):

    title = models.CharField(max_length=200)
    location = models.ForeignKey(Location, related_name='links')
    
    visible = models.BooleanField()
    position = models.IntegerField()

    def __unicode__(self):
        return u"{0}".format(self.title)


class LinkTranslation(models.Model):

    title = models.CharField(max_length=200)
    language = models.ForeignKey(Language, related_name='link_translations')

    link = models.ForeignKey(Link, related_name='translations')

    def __unicode__(self):
        return u"{0}".format(self.title)
