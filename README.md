# Mobot
Spanish bot dedicated to managing movie selections using JSON.

# Setup
To host Mobot, you will need two things:
- OMDb API key (Obtainable though [here](https://www.omdbapi.com/apikey.aspx))
- Discord bot Token (Obtainable through [here](https://discord.com/developers/home))

Having the token and API key, each will need to be added to `conf/.env`. *token* holds the Discord token, while *apikey* holds the OMDb API key (Self-explanatory, right?)

# Running
Having set up the API key and token, running the bot is as follows:
```sh
python bot.py
```
