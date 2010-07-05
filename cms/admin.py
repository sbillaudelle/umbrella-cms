from models import Page, PageTranslation, Location, Language, Link, LinkTranslation
from django.contrib import admin

admin.site.register(Language)
admin.site.register(Page)
admin.site.register(PageTranslation)
admin.site.register(Location)
admin.site.register(Link)
admin.site.register(LinkTranslation)
