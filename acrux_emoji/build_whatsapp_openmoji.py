# -*- coding: utf-8 -*-
import json


workspace = '/home/ediaz/trabajo/addons/Chat/'
folder = workspace + 'acrux_emoji/'
openmoji_dir = workspace + 'openmoji/'


def clean_dict(a):
    for i in a:
        i['emoji_qry'] = i['emoji']
        i['hexcode_qry'] = i['hexcode'].upper()


def clean_skin(a):
    skins = ['1F3FB', '1F3FC', '1F3FD', '1F3FE', '1F3FF']
    skins_emoji = ['\\U000' + x for x in skins]
    skins_emoji = [bytes(x, 'utf-8') for x in skins_emoji]
    skins_emoji = [x.decode('unicode_escape') for x in skins_emoji]
    for i in a:
        hexa = i['hexcode_qry'].split('-')
        hexa = list(filter(lambda x: x not in skins, hexa))
        i['hexcode_qry'] = '-'.join(hexa)
        i['emoji_qry'] = ''.join(list(filter(lambda x: x not in skins_emoji, i['emoji_qry'])))


def add_emoji(element, i, whatsapp_emoji_dict):
    element = element[0].copy()
    element['whatsapp_emoji'] = i['emoji']
    element['emoji'] = i['emoji']
    element['link'] = i['link']
    element['whatsapp_annotation'] = i['annotation']
    whatsapp_emoji_dict.append(element)


def get_hexa_code(char):
    unicode_str = char.encode('unicode_escape')
    unicode_str = unicode_str.decode('utf-8').upper()
    unicode_str = unicode_str.lstrip('\\U')
    unicode_str = unicode_str.lstrip('0')
    return unicode_str


def print_code(element):
    unicode_str = '-'.join([get_hexa_code(c) for c in element['emoji']])
    utf8_str = '-'.join(c.encode('utf-8').hex() for c in element['emoji'])
    utf16_str = '-'.join(c.encode('utf-16').hex() for c in element['emoji'])
    print(json.dumps(element, indent=2, ensure_ascii=False))
    print('size:%d utf8:%s utf16:%s unicode:%s' % (len(element['emoji']),
                                                   utf8_str, utf16_str, unicode_str))


def procesar(whatsapp_dict, whatsapp_emoji_dict, openmoji_dict, no_procesado):
    for i in whatsapp_dict:
        element = list(filter(lambda x: x['emoji_qry'] == i['emoji_qry'], openmoji_dict))
        if len(element) == 1:
            add_emoji(element, i, whatsapp_emoji_dict)
        else:
            element2 = list(filter(lambda x: x['hexcode_qry'] == i['hexcode_qry'], openmoji_dict))
            if len(element2) == 1:
                add_emoji(element2, i, whatsapp_emoji_dict)
            else:
                if len(element) == 0 and len(element2) == 0:
                    no_procesado.append(i)
                elif len(element) > 1 and len(element2) > 1:
                    raise Exception('no paso\nno se considero\nmuchos muchos\n')
                elif len(element) > 1 and len(element2) == 0:
                    raise Exception('no paso\nno se considero\nmuchos por emoji no por hexa')
                elif len(element) == 0 and len(element2) > 1:
                    raise Exception('no paso\nno se considero\nmuchos por hexa no por emoji\n')
                else:
                    raise Exception('no paso\nno se considero\nno deberia pasar\n')


lista = open(folder + 'list_whatsapp_emoji.json', 'r')
whatsapp_dict = json.loads(lista.read())
clean_dict(whatsapp_dict)
lista.close()

lista = open(openmoji_dir + '/data/openmoji.json', 'r')
openmoji_dict = json.loads(lista.read())
clean_dict(openmoji_dict)
lista.close()

whatsapp_emoji_dict = []
no_procesado = []
procesar(whatsapp_dict, whatsapp_emoji_dict, openmoji_dict, no_procesado)
if no_procesado:
    clean_skin(no_procesado)
    no_procesados2 = []
    procesar(no_procesado, whatsapp_emoji_dict, openmoji_dict, no_procesados2)
    if no_procesados2:
        print('con errores')
    else:
        print('bien')
        f = open(folder + 'acrux_whatsapp_emoji_large.json', 'w')
        f.write(json.dumps(whatsapp_emoji_dict, indent=2, ensure_ascii=False))
        f.close()
