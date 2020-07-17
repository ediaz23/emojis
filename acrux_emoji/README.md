Acrux Emoji
========
Scrips para generar los emoji que utiliza el chat, se deben correr varios scripts.

# bajar_emojin_whatsapp
    Baja la lista de los emoji de whatsapp desde emojipedia.org
# build_whatsapp_openmoji
    Construye acrux_whatsapp_emoji_large.json con toda la información
    de los emojis
# correr node acrux_build_sprite.js en el projecto openmoji-spritemap-generator
    Esto creara todos los sprites con los emojis
# copiar las imagenes, css a la carpeta emoji del modulo
# correr comprimir_json.py 
    para comprimir el json y copiarlo a la carpeta emoji del modulo