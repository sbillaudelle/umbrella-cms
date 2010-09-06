from django.db import models

class Setting(models.Model):

    key = models.CharField(max_length=200)
    value = models.CharField(max_length=200, blank=True)

    def __nonzero__(self):
        return self.id is not None


class Settings(object):

    def __init__(self):
        pass


    def get(self, key, default):

        try:
            setting = Setting.objects.filter(key=key).get()
            if setting:
                return setting.value
            else:
                return default
        except:
            return default


class Language(models.Model):

    name = models.CharField(max_length=50)
    code = models.CharField(max_length=8)

    def __init__(self, *args, **kwargs):
        models.Model.__init__(self, *args, **kwargs)
        settings = Settings()
        default_language_code = settings.get('default_language', 'en')
        if self.code == default_language_code:
            self.default = True
        else:
            self.default = False


    def __unicode__(self):
        return u"{0}".format(self.name)


class Page(models.Model):

    last_update = models.DateTimeField(auto_now=True)

    def title(self):
        settings = Settings()
        default_language_code = settings.get('default_language', 'en')
        default_language = Language.objects.filter(code=default_language_code).get()
        trans = self.translations.filter(language=default_language).get()
        return trans.title

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
