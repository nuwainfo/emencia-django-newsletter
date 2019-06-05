"""Utils for newsletter"""
import urllib.request, urllib.error, urllib.parse

from bs4 import BeautifulSoup
from django.core.urlresolvers import reverse

from emencia.django.newsletter.models import Link


def get_webpage_content(url):
    """Return the content of the website
    located in the body markup"""
    request = urllib.request.Request(url)
    page = urllib.request.urlopen(request)
    soup = BeautifulSoup(page)

    return soup.body.prettify()


def body_insertion(content, insertion, end=False):
    """Insert an HTML content into the body HTML node"""
    if not '<body>' in content:
        content = '<body>%s</body>' % content
    soup = BeautifulSoup(content)

    parsedHtml = BeautifulSoup(insertion)
    if parsedHtml.body:
        if end:
            soup.body.append(parsedHtml.body.findChildren()[0])
        else:
            soup.body.insert(0, parsedHtml.body.findChildren()[0])
    else:
        if end:
            soup.body.append(parsedHtml.findChildren()[0])
        else:
            soup.body.insert(0, parsedHtml.findChildren()[0])
        
    return soup.prettify()


def track_links(content, context):
    """Convert all links in the template for the user
    to track his navigation"""
    if not context.get('uidb36'):
        return content

    soup = BeautifulSoup(content)
    for link_markup in soup('a'):
        if link_markup.get('href'):
            link_href = link_markup['href']
            link_title = link_markup.get('title', link_href)
            link, created = Link.objects.get_or_create(
                url=link_href,
                defaults={'title': link_title}
            )
            link_markup['href'] = 'http://%s%s' % (
                context['domain'], 
                reverse(
                    'newsletter_newsletter_tracking_link',
                    args=[
                        context['newsletter'].slug,
                        context['uidb36'], context['token'],
                        link.pk
                    ]
                )
            )
    return soup.prettify()
