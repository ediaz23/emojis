// This runner is meant for customisation and to give an example of
// how multiple sprite sheets can be created with a single command.
//
const openemoji_dir = '../openmoji/'
const mojis = require('../acrux_emoji/acrux_whatsapp_emoji_large.json')
const asyn = require('async')
const generate = require('./index')
const generateIndex = require('./lib/htmlIndex')
const path = require('path')
const fs = require('fs')

const MODE = 'png' // out of { 'svg', 'png' }
const EMOJI_DIR_NAME = {
  png: 'color/72x72',
  svg: 'color/svg'
}

// Group emojis by their group name into an object.
// Use the group names as keys.
const mojiGroups = mojis.reduce((acc, moji) => {
  const groupName = moji.group
  if (!acc[groupName]) {
    acc[groupName] = []
  }
  acc[groupName].push(moji)
  return acc
}, {})

// Limit all groups to 8 * 16 emojis to avoid bus error 10.
Object.keys(mojiGroups).forEach(groupName => {
    let emoji_list = mojiGroups[groupName];
    let i, row = 34;
    for(i = 0; i * row * 8 < emoji_list.length; ++i) {
        if (i) {
            mojiGroups[groupName + '_' + i] = emoji_list.slice(i * row * 8, (i + 1) * row * 8)
        } else {
            mojiGroups[groupName] = emoji_list.slice(i * row * 8, (i + 1) * row * 8)
        }
    }
  
})

// For each group, run sheet generator.
// Sheet generation is asynchronous operation, thus @caolan/async is used.
asyn.eachSeries(Object.keys(mojiGroups), (groupName, next) => {
  const mojiGroup = mojiGroups[groupName]
  generate({
    mode: MODE,
    name: groupName,
    emojis: mojiGroup,
    emojiDir: path.join(openemoji_dir, EMOJI_DIR_NAME[MODE]),
    targetDir: path.join(__dirname, 'target'),
    url_img: '../img/',
    emojiSize: 72,
    columns: 8
  }, next)
}, (err) => {
  if (err) {
    console.error(err)
    return
  }

  // Generate an index page to browse the generated sheets.
  const indexHtml = generateIndex(mojiGroups, {
    mode: MODE
  })
  const indexPath = path.join(__dirname, 'target', 'index.html')
  fs.writeFileSync(indexPath, indexHtml)

  console.log('Finished successfully.')
})
