# takt_authenticator
Telegram bot for registrating people on event, with generating unique links.
## There are two bots: final_bot and link_gen_bot

## final_bot
What it does:
* validating token
* checking if a person is subscribed on a specific channel
* registring person to google spreadsheet via google API

## link_gen_bot
What it does:
* generates infinite amount of unique links
* talks to google spreadsheet, so that links are not duplicated when genereted
