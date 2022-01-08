# **Vulkan**

A multi-purpose Discord bot, including music, written in Python and supports Youtube and Spotify sources for playing. Vulkan was designed so that everyone could fork this project and use it, including a 24/7 host on Heroku.


Vulkan is also able to get data from Warframe and send it to users, get random phrases and handle random operations to help users decide what to do.


## **Prerequisites:** 

### **API Keys**
 * Your Discord Application - [Discord](https://discord.com/developers)
 * You own Spotify Keys - [Spotify](https://developer.spotify.com/dashboard/applications)

    - This information must be stored in an .env file, explained further.

### **Requirements**
- Installation of Python 3.8+ and the dependencies in the requirements.txt file.
```
pip install -r requirements.txt
```


-  Installation of FFMPEG

    *FFMPEG must be configured in the PATH for Windows users. Check this [YoutubeVideo](https://www.youtube.com/watch?v=r1AtmY-RMyQ&t=114s&ab_channel=TroubleChute).*

### **.Env File Example**
This is an example of how your .env file (located in root) should look like, those API url could be the same.
```
CETUS_API=https://api.warframestat.us/pc/cetusCycle
CAMBION_API=https://api.warframestat.us/pc/cambionCycle
FISSURES_API=https://api.warframestat.us/pc/fissures
PHRASES_API='http://api.forismatic.com/api/1.0/?method=getQuote&key=457653&format=json&lang=en'

BOT_TOKEN=Your_Own_Bot_Token
SPOTIFY_ID=Your_Own_Spotify_ID
SPOTIFY_SECRET=Your_Own_Spotify_Secret
SECRET_MESSAGE=Your_Own_Secret_Message

```

### **Config File**
The config file, located in ```./config``` folder doesn't require any change, but if you acquire the knowledged of how it works, you can change it to the way you want.


### **Initialization**
- Go to [Discord](https://discord.com/developers) and invite your Bot to your own server
- Run ```python main.py``` in console to start


## **Heroku**
To run your Bot in Heroku 24/7, you will need the Procfile located in root, then follow the instructions in this [video](https://www.youtube.com/watch?v=BPvg9bndP1U&ab_channel=TechWithTim). In addition, also add these two buildpacks to your Heroku Application:

    - https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git

    - https://github.com/xrisk/heroku-opus.git


#  **Music**
- Play musics from Youtube and Spotify Playlists
- Controll loop of one or all musics
- Allow realocating musics in the queue
- Play musics in queue randomly

### Commands
```!play [title, spotify_url, youtube_url]``` - Start playing song in Discord

```!resume``` - Resume the song player

```!pause``` - Pause the song player

```!move [x, y]``` - Change the musics in position x and y in Queue

```!skip``` - Skip the currently playing song

```!stop``` - Stop the playing of musics

```!queue``` - Show the musics list in queue

```!shuffle``` - Shuffle the songs in queue

```!remove [x]``` - Remove the song in position x

```!reset``` - Reset the player, recommended if any error happen 

```!loop [one, all, off]``` - Control the loop of songs 

```!np``` - Show information of the currently song 

```!clear``` - Clear the songs in queue, doesn't stop the player 


## License
- This program is free software: you can redistribute it and/or modify it under the terms of the [MIT License](https://github.com/RafaelSolVargas/Vulkan/blob/master/LICENSE).


## Contributing
 - If you are interested in upgrading this project i will be very happy to receive a PR or Issue from you. See TODO project to see if i'm working in some feature now.  


## Acknowledgment
 - See the DingoLingo [project](https://github.com/Raptor123471/DingoLingo) from Raptor123471, it helped me a lot to build Vulkan.
