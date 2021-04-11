# mcveighglazing - a simple HAPI webapp
This was a repo I created during development of a full stack website for my fathers business.

It is built using node js (HAPI framework), and consists of just 1 page with a contact form which hooks into his email inbox

## Prerequisites
You will need to have node and npm installed to run this app

## Setup
From the root directory run the following commands
```
npm run build
cp .env.example .env
```

Then, open the file `.env` and complete the missing fields with your own configuration for SMTP

Now, you should be able to run the server by running `npm start`. You can visit the app at http://localhost:3000
