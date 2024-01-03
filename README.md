# Discord Scraper

This is a discord bot that will help look at user interactions.

I am assuming that you have created your own discord bot and have a bot token

## Using the bot

1) Create a file called `config.py` and add...
``` python
# config.py
BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'

```

2) Add the bot to the server you want to look at by going to the OAuth2 section 
of your bot's application page and copying the generated url.

3) After this, run the `setup.sh` script to create a python localenv.

4) Finally, run the `src.py` file. This will prompt you to select a server and a user. Then, 
it will gather all examples of the user replying to other users in the server and write them 
to a `.pkl` file