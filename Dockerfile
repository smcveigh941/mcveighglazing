FROM node:12.22.1-alpine3.12

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app

RUN npm ci --only=production && chown node /usr/src/app

USER node

EXPOSE 3000

CMD [ "npm", "start" ]
