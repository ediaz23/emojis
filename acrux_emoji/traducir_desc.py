# -*- coding: utf-8 -*-

import json

folder = '/home/ediaz/trabajo/addons/Chat/acrux_chat/static/src/emoji/'


def traducir(words_to_trans, word_cache):
    return ' '.join(words_to_trans)


lista_traducida = open(folder + 'list_traducida.csv', 'w')
lista = open(folder + 'list_emoticon.csv', 'r')
f_cache = None
word_cache = None

try:
    f_cache = open(folder + 'word_translated_cache.txt', 'r+')
    content = f_cache.read()
    f_cache.seek(0)
    word_cache = json.loads(content)
except Exception as _e:
    f_cache = open(folder + 'word_translated_cache.txt', 'w')
    word_cache = {}

for linea in lista:
    words_to_trans = linea.split(',')[0].split(' ')
    new_line = linea.rstrip('\n') + ',' + traducir(words_to_trans, word_cache) + '\n'
    lista_traducida.write(new_line)
    break

f_cache.write(json.dumps(word_cache, indent=2))
lista.close()
lista_traducida.close()
