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
* filters : Function and objects for image filters ;
* friends : Function and objects to manage friends and followers;
* hashtags : Function and objects to manage hashtags ;
* instagram : Function and objects for Instagram ;
* instagramAPI : The instagram API ;
* learning : Functions and objects for image and text classification ;
* media : Functions and objects to manage medias ;
* patterns : Object patterns ;
* tools : Tools;

## Authors

* **Nils Schaetti** - *Initial work* - [nschaetti](https://github.com/nschaetti/)

## License

This project is licensed under the GPLv3 License - see the [LICENSE](LICENSE) file
for details.

## Configuration

### Configuration file

pyInstaBot takes its configuration in a JSON file which looks as follow :

```
{
    "instagram" :
	{
        "username": "",
        "password": "",
		"data_path": ""
    },
	"scheduler" :
	{
		"sleep": [6, 13]
	},
	"hashtags":
	[
	],
	"friends" :
	{
		"max_new_followers" : 40,
		"max_new_unfollow" : 40,
		"interval" : [30, 45],
		"ratio" : 0.8
	},
	"post":
	{
		"post_interval": [30, 90],
		"like_interval": [0, 4],
		"comment_interval": [0, 8],
        "max_posts": 24,
        "max_likes": 700,
        "max_comments": 300,
		"languages": ["en", "fr"],
		"comments": ["Nice!", "Nice feed!", "Keep going", "Good work", "👊🏻😎", "😅😅😅", "❤❤❤❤", "Nice! 😅😅😅", "Keep going 😅😅😅"]
	},
	"forbidden_words" :
	[
	]
}
```

Their is two required sections :
* Database : contains the information to connect to the MySQL database (host, username, password, database)
* Instagram : contains the information for the Twitter API (auth and access tokens)

## Command line

### Launch executors

pyInstaBot launch an executor thread for each action type. You can launch the executor daemon that way :

    python -m pyInstaBot execute --session session_public.json --config nilsbot.json

### Find post to like

To find post to like :

    python -m pyInstaBot find-likes --session session_public.json --config nilsbot.json --model .

### Find post to comment

To find post to comment :

    python -m pyInstaBot find-comments --session session_public.json --config nilsbot.json --model .

### Find users to follow

To find new users to follow :

    python -m pyInstaBot find-follows --session session_public.json --config nilsbot.json --model .

### Find users to unfollow

To find obsolete users to unfollow :

    python -m pyInstaBot find-unfollows --session session_public.json --config nilsbot.json --model .

### Update friends

To update the list of friends in the database :

    python -m pyInstaBot friends --session session_public.json --config nilsbot.json --update

### Add medias

To add all medias in a directory with a common caption :

    python -m pyInstaBot medias --session session_public.json --config nilsbot.json --add ~/images/ --caption ~/images/caption --loop

The loop argument will repost the medias multiple time. To add only one image :

    python -m pyInstaBot medias --session session_public.json --config nilsbot.json --add ~/images/im.jpg --caption ~/images/caption --loop

## Development

### Files

* [pyInstaBot/__main__.py](__main__.py) : Main Python file;
* [pyInstaBot/add_medias.py](add_medias.py) : Add medias to the database ;
* [pyInstaBot/apply_filter.py](apply_filters.py) : Apply filter to images ;
* [pyInstaBot/clean_medias.py](clean_medias.py) : Clean all medias in the DB ;
* [pyInstaBot/create_database.py](create_database.py) : Create database structure ;
* [pyInstaBot/execute_actions.py](execute_actions.py) : Execute actions from the DB ;
* [pyInstaBot/find_follows.py](find_follows.py) : Find users to follow ;
* [pyInstaBot/find_locations.py](find_locations.py) : Find locations ;
* [pyInstaBot/find_medias.py](find_medias.py) : Find medias to like/comment ;
* [pyInstaBot/find_unfollows.py](find_unfollows.py) : Find users to unfollow ;
* [pyInstaBot/hashtag_analysis.py](hashtag_analysis.py) : Hashtag analysis functions;
* [pyInstaBot/setup.py](setup.py) : Installation script ;
* [pyInstaBot/update_statistics.py](update_statistics.py) : Update account statistics ;

