<p align="center"><img src="docs/images/pyinstabot.png" /></p>

--------------------------------------------------------------------------------
An Instagram bot and library written in Python to publish content automatically.

Join our community ! Chat with us on Gitter and join the Google Group to collaborate with us.

This repository consists of:

* config : Configuration file management;
* data : 
* db : MySQL database management;
* docs : Documentation;
* executor : Function and objects to execute actions;
* filters : 
* followers : 
* friends : Function and objects to manage friends and followers;
* gui : 
* hashtags : 
* instagram : 
* instagramAPI : 
* learning : 
* media : 
* patterns : 
* tools : Tools;

## Authors

* **Nils Schaetti** - *Initial work* - [nschaetti](https://github.com/nschaetti/)

## License

This project is licensed under the GPLv3 License - see the [LICENSE](LICENSE) file
for details.

## Configuration

### Configuration file

pyTweetBot takes its configuration in a JSON file which looks as follow :

```
javascript
{
```

Their is two required sections :
* Database : contains the information to connect to the MySQL database (host, username, password, database)
* Twitter : contains the information for the Twitter API (auth and access tokens)

## Command line

### Launch executors

    python -m pyInstaBot execute --session /home/schaetti/bots/pyinstabot/nils-config/session_public.json --config /home/schaetti/bots/pyinstabot/nils-config/nilsbot.json

### Find post to like

    python -m pyInstaBot find-likes --session ~/bots/pyinstabot/nils-config/session_public.json --config ~/bots/pyinstabot/nils-config/nilsbot.json --model .

### Find post to comment


### Find users to follow

    python -m pyInstaBot find-follows --session ~/bots/pyinstabot/nils-config/session_public.json --config ~/bots/pyinstabot/nils-config/nilsbot.json --model .

### Find users to unfollow

    python -m pyInstaBot find-unfollows --session ~/bots/pyinstabot/nils-config/session_public.json --config ~/bots/pyinstabot/nils-config/nilsbot.json --model .

### Update friends

    python -m pyInstaBot friends --session ~/bots/pyinstabot/nils-config/session_public.json --config ~/bots/pyinstabot/nils-config/nilsbot.json --update

### Add medias

    python -m pyInstaBot medias --session ~/bots/pyinstabot/nils-config/session_public.json --config ~/bots/pyinstabot/nils-config/nilsbot.json --add ~/images/IQLA2017/ --caption ~/images/IQLA2017/caption --loop

## Development

### Files


