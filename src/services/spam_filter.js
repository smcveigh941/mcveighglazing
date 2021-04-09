const scan = (message) => {
  return blacklist.map(item => new RegExp(`\\b${item}\\b`)).some(item => item.test(message))
}

const blacklist = [
    'sex',
    'casino',
    'gamble',
    'virus',
    'trojan',
    'http://',
]

module.exports = {
  scan: scan
}