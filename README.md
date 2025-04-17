# HabitsApi

HabitsApi is a backend habits tracking API integrated with Telegram. Based on "Atomic habits" by James Clear it helps
you to make good habits a part of your life.

## Server Setup
1. Connect to your server
```commandline
ssh user_name@your_server_ip
```
2. Run necessary updates
```commandline
sudo apt update && sudo apt upgrade
```
3. Set up firewall and open necessary ports
```commandline
sudo ufw status
sudo ufw enable #in case firewal is turned off
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp
```

## Installation

1. Clone the repository:
```commandline
git clone https://github.com/obladishka/habits_api.git
```
2. Go to project directory and set up env variables according to .env.sample:
```commandline
cd habits_api/
nano .env
```
3. Start the container:
```commandline
docker-compose up
```
4. Congratulations! The project is set up successfully! To enjoy all the features go to http://158.160.177.36/habits
and create a user account.

## Automatic deployment

1. Clone the repository to your project and make some amendments:
```commandline
git clone https://github.com/obladishka/habits_api.git
```
2. Create a new git repository and add all necessary environmental variables to secrets.
3. Push your project to the repository. GitHUB Actions will automatically test your project and deploy it to server if everything is correct.

## API Documentation

After starting the container, access the API documentation at:

Swagger UI: http://158.160.172.16/api/schema/
Redoc UI: http://158.160.172.16/api/docs/
```