from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^\+admin/api$', 'cms.views.admin_api'),
    (r'^\+admin/languages$', 'cms.views.admin_languages'),
    (r'^\+admin/pages$', 'cms.views.admin_list_pages'),
    (r'^\+admin/pages/(?P<page>[0-9]+)$', 'cms.views.admin_page'),
    (r'^\+admin/pages/(?P<page>[0-9]+)/edit/(?P<lang>.+)$', 'cms.views.admin_page_edit'),
    (r'^\+admin$', 'cms.views.admin_index'),
    (r'^(?P<path>.+)', 'cms.views.view'),
    (r'', 'django.views.defaults.page_not_found')
)
