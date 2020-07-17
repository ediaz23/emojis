# -*- coding: utf-8 -*-
import json
from subprocess import Popen, PIPE


workspace = '/home/ediaz/trabajo/addons/Chat/'
output_dir = workspace + 'acrux_chat/static/src/emoji/json/'
input_dir = workspace + 'openmoji-spritemap-generator/target/'
keep = ["emoji", "hexcode", "group", "subgroups", "tags", "skintone_combination",
        "skintone_base_emoji", "skintone_base_hexcode", "order", "whatsapp_emoji",
        "whatsapp_annotation"]

pr = Popen('ls %s*.json' % input_dir, stdout=PIPE, shell=True)
json_list, error = pr.communicate()
pr.wait()
json_list = json_list.decode('utf-8').rstrip()
json_list = json_list.split('\n')
for i in json_list:
    name = i.split('/')[-1]
    f = open(i, 'r')
    content = f.read()
    f.close()
    data = json.loads(content)
    for emoji in data['emojis']:
        new_dict = {k: emoji['emoji'][k] for k in keep}
        emoji['emoji'] = new_dict
    f = open(output_dir + name, 'w')
    f.write(json.dumps(data, indent=2, ensure_ascii=False))
    f.close
