from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe

import json

from models import Page, PageTranslation, Link, LinkTranslation, Location, Language

from languages import languages as languages

def view(request, path):

    lang_code = None

    if request.META.has_key('HTTP_ACCEPT_LANGUAGE'):
        preferred_langs = [lang.split(';')[0].strip() for lang in request.META['HTTP_ACCEPT_LANGUAGE'].split(',')]
        # TODO: Implement priority handling (http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html)
        lang_code = preferred_langs[0]

    try:
        lang = Language.objects.filter(code=lang_code).get()
    except:
        lang = None

    location = Location.objects.filter(location=path).get()
    page = location.page

    _links = Link.objects.filter(visible=True).order_by('position')
    links = []

    if lang:
        try:
            page = PageTranslation.objects.filter(language=lang, page=page).get()
        except:
            pass

        for link in _links:
            try:
                t = LinkTranslation.objects.filter(language=lang, link=link).get()
                t.location = link.location
                links.append(t)
            except:
                links.append(link)

    content = mark_safe(page.content)
    title = page.title

    return render_to_response('view.html', {
        'content': content,
        'title': title,
        'page': page,
        'links': links,
        })


def admin_api(request):

    if request.POST['method'] == 'add_location':
        l = Location()
        l.location = request.POST['location']
        l.page = Page.objects.filter(id=request.POST['page']).get()
        l.save()
        return HttpResponse(json.dumps({
            'location': l.location,
            'id': l.id,
            }))
    elif request.POST['method'] == 'remove_location':
        l = Location.objects.filter(id=request.POST['location']).get()
        l.delete()
        return HttpResponse(json.dumps({
            'id': request.POST['location'],
            }))
    elif request.POST['method'] == 'add_language':
        lang = Language()
        lang.code = request.POST['code']
        lang.name = request.POST['name']
        lang.save()
        return HttpResponse('true')
    elif request.POST['method'] == 'remove_language':
        lang = Language.objects.filter(code=request.POST['code']).get()
        lang.delete()
        return HttpResponse('true')
    elif request.POST['method'] == 'save_page':
        translation = PageTranslation.objects.filter(id=request.POST['id']).get()
        translation.content = request.POST['content']
        translation.save()
        return HttpResponse('true')
    else:
        print request.POST
        return HttpResponse('')


def admin_list_pages(request):

    pages = Page.objects.all()
    return render_to_response('administration/pages.html', {'pages': pages})


def admin_index(request):
    return render_to_response('administration/index.html', {})


def admin_languages(request):

    langs = []

    for c, l in languages.iteritems():
        if Language.objects.filter(code=c):
            s = True
        else:
            s = False
        langs.append((c, l, s))

    langs.sort()

    return render_to_response('administration/languages.html', {'languages': langs})


def admin_page(request, page):

    p = Page.objects.filter(id=page).get()

    langs = Language.objects.all()

    return render_to_response('administration/page.html', {
        'page': p,
        'languages': langs
        })


def admin_page_edit(request, page, lang):

    p = Page.objects.filter(id=page).get()

    #if request.POST.has_key('editor'):
    #    if lang:
    #        t = p.translations.filter(language=Language.objects.filter(code=lang).get()).get()
    #        t.content = request.POST['editor']
    #        t.save()
    #    else:
    #        p.content = request.POST['editor']
    #         p.save()

    try:
        translation = p.translations.filter(language=Language.objects.filter(code=lang).get()).get()
    except:
        translation = PageTranslation()
        translation.page = p
        translation.language = Language.objects.filter(code=lang).get()
        translation.save()
    title = translation.title
    content = translation.content

    langs = Language.objects.all()

    return render_to_response('administration/edit.html', {
        'page': p,
        'translation': translation,
        'title': title,
        'content': content,
        'languages': langs
        })
