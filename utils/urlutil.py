__author__ = 'erik'

from urlparse import urlparse


def prepare_url(url):
    purl = urlparse(url)
    return {'url': purl.geturl(), 'host': purl.scheme + '://' + purl.netloc, 'path': purl.path}


