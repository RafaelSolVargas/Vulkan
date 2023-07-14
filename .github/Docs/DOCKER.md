<h1 align="center">Docker</h1>

This bot can be easily deployed using Docker.

## **Requirements**
To run this project in a Docker container you must have Docker and Docker Compose installed in your machine. Find how to install Docker in your machine [here](https://docs.docker.com/get-docker/) and find how to install Docker Compose in your machine [here](https://docs.docker.com/compose/install/).

Once you have Docker and Docker Compose installed in your machine, clone or download this repository and follow the instructions below.

## **Running the Bot**
To run the bot in a Docker container, you must first create a `.env` file in the root of the project if there isn't one already. You will need to change the parameters in the `.env` file to your own parameters. You can find an example of a `.env` file [here](.env.example). You will also be able to change the settings in that environment file as explained in the [Settings page](.github/Docs/SETTINGS.md). 

**If any of the following commands fail, try without a dash between docker and compose.**

To run the bot, simply execute the following command in the root of the project:
```bash
docker-compose up -d
```
This will build the Docker image and run the bot in a Docker container. The `-d` flag is used to run the container in detached mode, which means that the container will run in the background. If you want to see the logs of the container, you can run the following command:
```bash
docker-compose logs -f
```

To stop the container, run the following command:
```bash
docker-compose down
```
## **Updating the Bot**
To update the bot, you must first stop the container as explained in the previous section. Then, you must pull the latest changes from the repository, in any way you want. Finally, you must build the Docker image again and run the container again. To do this, run the following commands:
```bash
docker-compose build
docker-compose up -d
```