#!/usr/bin/env python

from lxml import html
import shutil
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

def get_id(path):
    return path.split('/')[-1]

def download_image(url, destination):
    response = requests.get(url, stream=True)
    with open(destination, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    return destination

def do_a_crawling(path):
    page = get_page(path)
    body = get_body(page)

    return {
            'id': get_id(path),
            'image': get_image(body),
            'description': get_description(body),
            'next_path': get_next_path(body),
            }

def save_results(crawl):

    # download image
    image_url = crawl['image']
    response = requests.get(image_url, stream=True)
    image_destination = '%s.jpg' % crawl['id']
    with open(image_destination, 'wb') as handle:
        shutil.copyfileobj(response.raw, handle)

    text_destination = '%s.txt'

    # save text
    with open(text_destination, 'w') as handle:
        print >> handle, crawl['description']


path = '/dnd'
while True:
    resp = do_a_crawling(path)
    path = resp['next_path']
    crawl = do_a_crawling(path)

    print crawl

    save_results(crawl)
