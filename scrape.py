#!/usr/bin/env python

from lxml import html
import requests

def get_url(path, base='http://www.vice.com'):
    return '%s/%s' % (base, path)

def get_image(body):
    image = body.xpath('//img')[0]
    return image.items()[0][1]

def get_description(body):
    return body.xpath('//p')[1].text_content()

def get_next_path(body):
    return body.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "right", " " ))]')[1].values()[0]

def get_page(url):
    return requests.get(get_url(url))

def get_body(page):
    return html.fromstring(page.text)

def do_a_crawling(path):
    page = get_page(path)
    body = get_body(page)

    return {
            'image': get_image(body),
            'description': get_description(body),
            'next_path': get_next_path(body)
            }


path = '/dnd'
while True:
    resp = do_a_crawling(path)
    path = resp['next_path']
    print do_a_crawling(path)
