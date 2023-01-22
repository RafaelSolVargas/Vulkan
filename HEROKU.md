<h1 align="center">Configuring Heroku</h1> 

> Heroku doesn't offer free services anymore 

Nobody wants to run the Vulkan process on their machine, so we host the process on Heroku, <s>a cloud platform that contains free</s>.<br>
To configure the Vulkan to run in your Heroku account you will need to:

- Create an application project in Heroku.
- Configure the environment variables in your application.
- Add these buildpacks to your application:
    
    ```
    - heroku/python
    - https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
    - https://github.com/xrisk/heroku-opus.git
    ```
    The order shown above is exactly the upside-down order that Buildpacks should appear in Heroku.
- Set the heroku stack to be `heroku-20`. <br>
    As shown in this issue: [Issue](https://github.com/RafaelSolVargas/Vulkan/issues/25) the heroku-buildpack doesn't work properly with the heroku application Stack set as above `heroku-20`.

<br>

This [Youtube Video](https://www.youtube.com/watch?v=BPvg9bndP1U&ab_channel=TechWithTim) shows the process of hosting a Bot in Heroku.

You can also fork this project and set in Heroku to your application automatically deploy when your project receive a new commit, and then control when new versions of Vulkan become available to your Bot. 