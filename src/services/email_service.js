const mailer = require('nodemailer')
const logger = require('winston').loggers.get('logger')
const config = require('getconfig')

const sendMessage = async (name, telephone, email, message) => {
  const transporter = mailer.createTransport({
    host: config.mail.server,
    port: config.mail.port,
    secure: config.mail.secure,
    auth: {
      user: config.mail.user,
      pass: config.mail.password,
    }
  });

  transporter.sendMail({
    from: config.mail.user,
    to: config.mail.recipients,
    subject: 'Job Query',
    html: `${name} has sent you a message using the website.<br/>Phone Number: ${telephone}<br/>Email: ${email}<br/>Message: <br/> ${message}`,
  })
  .then(info => logger.info("Message sent: %s", info.messageId))
  .catch(error => logger.error(error.toString()));
}

module.exports = {
  sendMessage: sendMessage
}
