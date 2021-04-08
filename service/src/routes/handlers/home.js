const _ = require('lodash')
const logger = require('winston').loggers.get('logger')

const emailService = require('../../services/email_service')
const spamFilter = require('../../services/spam_filter')

const home = () => {
  const GET = async (request, h) => {
    return h.view('pages/home')
  }

  const POST = async (request, h) => {
    const payload = request.payload

    if (!_.isEmpty(payload.honeypot)) {
      logger.warn('Honeypot activated. A bot is trying to use the contact form')
      return h.response('Bots are not allowed on this page').code(403)
    }

    if (spamFilter.scan(payload.message)) {
      logger.warn(`Spam detected from ${payload.email}/${payload.telephone}: ${payload.message}`)
      return h.response('No spam allowed').code(400)
    }

    await emailService.sendMessage(payload.name, payload.telephone, payload.email, payload.message)

    return h.response('Message sent successfully!').code(200)
  }

  return {
    GET,
    POST
  }
}

module.exports = {
  handlers: home
}
