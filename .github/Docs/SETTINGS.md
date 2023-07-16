<h1 align="center">Settings</h1> 


## Important Parameters
- Bot Prefix
- Auto Disconnect When Alone
- Specific Process for each Player
- Maximum songs downloading at a time
- Maximum songs in a Queue Page

All parameters can be modified in the .env file or in an environment variable.
Here is a sample of the .env file:

```env
BOT_TOKEN=Your_Own_Bot_Token
SPOTIFY_ID=Your_Own_Spotify_ID
SPOTIFY_SECRET=Your_Own_Spotify_Secret
BOT_PREFIX=Your_Wanted_Prefix_For_Vulkan
SHOULD_AUTO_DISCONNECT_WHEN_ALONE=True #all settings can be set like this
#etc... All settings can be set this way
```


### **Bot Prefix**
The Bot Prefix is just a string that must be passed as prefix when calling any Bot command from the Discord.
To change that you must: <br> 
- Change the property BOT_PREFIX in the .env file or in an environment variable to what you want to.

### **Auto Disconnect**
As a result of the [Issue 33](https://github.com/RafaelSolVargas/Vulkan/issues/33) you can configure if the Bot will auto disconnect when being alone in the voice channel. The default configuration is to disconnect within 300 seconds if it finds out no one is currently listing to it.
To change that you must: <br> 
- Change the property SHOULD_AUTO_DISCONNECT_WHEN_ALONE in the .env file or in an environment variable to False

### **Multiprocessing or Threading**
As a result of the [Issue 35](https://github.com/RafaelSolVargas/Vulkan/issues/35) you can configure if the Bot will create a specific Python Process for each Player (Guild) that he is playing songs or all will happen in the Main Process. The Default behavior is to create a new process.
To change that you must: <br> 
- Change the property SONG_PLAYBACK_IN_SEPARATE_PROCESS in the .env file or in an environment variable to False

### **Maximum Downloading Quant**
The download of songs can be very fast or very slow, the faster it is the slower the response time for any command (during the download) is higher, (including the playback quality), because there will be a Task for each song. But it's possible to set up this variable to slow the download and keep the response time better. 
To change that you must: <br> 
- Change the property MAX_DOWNLOAD_SONGS_AT_A_TIME in the .env file or in an environment variable to what you want to.

### **Maximum Songs In Queue Page**
When the ```Queue``` command is called, the current song playlist is presented in the Discord, you can configure how many songs you will want to show in each page.
To change that you must: <br> 
- Change the property MAX_SONGS_IN_PAGE in the .env file or in an environment variable to what you want to.