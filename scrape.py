#!/usr/bin/env python

from lxml import html
import shutil
import requests
import errno
import os

def save_dir(p, d='out'):
    out = os.path.join(d, p)
    try:
        os.mkdir(d)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise e
    print out
    return out

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

def is_do(path):
    res = path.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "dnd-tagline", " " ))]')[0].text_content().strip()
    if res == "don't":
        return False
    elif res == 'do':
        return True
    else:
        print 'WTF? %s' % res

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
            'do': is_do(body)
            }

def save_results(crawl):

    # download image
    image_url = crawl['image']
    response = requests.get(image_url, stream=True)
    image_destination = '%s.jpg' % crawl['id']
    with open(save_dir(image_destination), 'wb') as handle:
        shutil.copyfileobj(response.raw, handle)

    # save text
    text_destination = '%s.txt' % crawl['id']
    with open(save_dir(text_destination), 'w') as handle:
        print >> handle, crawl['description']

    # save do or dont status
    do_or_dont = '%s.status' % crawl['id']
    with open(save_dir(do_or_dont), 'w') as handle:
        print >> handle, crawl['do']

    return crawl


# start crawling
path = '/dnd'
while True:
    resp = do_a_crawling(path)
    path = resp['next_path']
    crawl = do_a_crawling(path)

    print crawl

    save_results(crawl)
