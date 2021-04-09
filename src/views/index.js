const Path = require('path')
const moment = require('moment')
const handlebars = require('handlebars')

const defaultContext = {
  assetPath: '/public',
  currentYear: moment().year()
}

module.exports = {
  engines: {
    html: handlebars
  },
  relativeTo: __dirname,
  path: Path.join(__dirname, ''),
  layoutPath: Path.join(__dirname),
  layout: 'view_template',
  context: defaultContext
}
