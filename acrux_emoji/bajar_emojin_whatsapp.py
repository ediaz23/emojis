# -*- coding: utf-8 -*-
from lxml import etree
import requests
import json

url_base = 'https://emojipedia.org'
workspace = '/home/ediaz/trabajo/addons/Chat/'
folder = workspace + 'acrux_emoji/'


def open_or_donwload(url_str):
    url_dir = 'html/' + url_str.replace('/', '') + '.html'
    f = None
    try:
        f = open(folder + url_dir, 'r')
    except Exception as _e:
        f = open(folder + url_dir, 'w+')
        r = requests.get(url_base + url_str)
        f.write(r.text)
        f.seek(0)
    return f


list_emoji = []
f = open_or_donwload('/whatsapp/')
parser = etree.HTMLParser()
tree = etree.parse(f, parser)
r = tree.xpath('//ul[@class="emoji-grid"]')
emoji_set = set()
for i in r[0].iterchildren():
    for a in i.iterchildren():
        sub_f = open_or_donwload(a.get('href'))
        sub_tree = etree.parse(sub_f, parser)
        x = sub_tree.xpath('//title')[0]
        split = x.text.split(' ')
        caracter = split[0]
        name = ' '.join(split[1:-1])
        code = ''
        x = sub_tree.xpath('//h2')
        for h2 in x:
            if h2.text == 'Codepoints':
                ul = h2.getnext()
                code_list = []
                for y in ul.iter('a'):
                    code = y.text.split(' ')
                    code = code[len(code) - 1]
                    code = code.lstrip()
                    code = code.lstrip('U+')
                    code_list.append(code)
                code = '-'.join(code_list)
                break
        if caracter not in emoji_set:
            list_emoji.append({'emoji': caracter,
                               'hexcode': code,
                               'annotation': name,
                               'link': a.get('href'),
                               })
            emoji_set.add(caracter)
        else:
            print('si filtro algo ' + caracter)
        sub_f.close()
f.close()
lista = open(folder + 'list_whatsapp_emoji.json', 'w')
lista.write(json.dumps(list_emoji, indent=2, ensure_ascii=False))
lista.close()
