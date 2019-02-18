
# IOT CA2 Smart Security [![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://demihickman.tk/) [![Website shields.io](https://img.shields.io/website-up-down-green-red/http/shields.io.svg)](https://demihickman.tk/) [![HitCount](http://hits.dwyl.io/ThePikachu/IOT_CA2_Public.svg)](http://hits.dwyl.io/ThePikachu/IOT_CA2_Public)

> Project Developed to Secure Rooms using IoT (RFID Card Readers, Live Cams and Many More...) <br/>View the web interface at https://demihickman.tk/

<img src="/Documents/github_images/finalsetup.jpg" alt="Project" width="400">
<img src="/Documents/github_images/raspberrypi_startup.gif" alt="Raspberry Pi Startup" width="100%">


## Table of Contents
- [Introduction](#introduction)
- [Fritzing Diagram](#fritzing)
- [Features](#features)
- [Libraries](#builtwith)
- [Setup](#setup)
- [Bot Setup](#bot)
- [Demo Video](#video)
- [Documentation](#tutorial)
- [Authors](#authors)
- [Acknowledgments](#ack)

<a name="introduction"></a>
## Introduction
The application, **Smart Security**, allow the administrator/users to manage their room security, with motion detection and video recording, the administrator can add unlimited amount of rooms provided there is enough hardware. Each hardware has a RFID card reader, to allow access to room, a temperature sensor to monitor the room’s temperature, a LED screen to display room name and messages to user, a motion sensor & camera. Administrator can keep track & allow specific card to access certain rooms, the motion sensor will be disarmed if room is currently being accessed. Upon any irregularity such as motion detected , the application will start a video recording and will be recorded down into a file and it will notify the administrator through telegram with the video.

The **admin web interface** will allow the administrator view historial temperature, access history & motion detected recordings. Also, they can manage each room and view access rights requests of users as well as approve/reject them

The **user web interface** will allow users to view live feed of the iot sensor data and, request for a RFID card reader and request for access rights to the rooms for their RFID card reader.

<a name="fritzing"></a>
## Fritzing Diagram
<img src="/Documents/IoT_bb.jpg" alt="Fritzing" width="70%">


<a name="features"></a>
## Features
### General Features
* Web Application and Database is hosted on AWS
* IOT AWS as broker for mqtt emission and subscription
* Admin and Public Interface

### IOT Features
* Currently running on 3 Raspberry Pis and 2 Matrix Creator
* Temperature sensor is using mqtt to transmit its values
* RFID card reader
* LED screen display to display messages
* Motion sensor and camera
* Light sensor and humidity sensor

### Web Application Features
* Login and Registration
* Different Dashboards depending on whether user is an Admin or Public User
* Admin Features
  - Display 5 interactive graphs of sensor data
  - Add, manage and delete rooms
  - Add, manage and delete access rights for public users
  - Approve, Reject and View access rights requests from public users
* Public Features
  - Live Cam retrieve image of room from AWS S3
  - Display live values of the sensors data (humidity, temperature, light)
  - Apply for a RFID card
  - Request access for rooms
  - View access rights for rooms

### Bot Features
* Features a discord bot that can be added to any server to let people know which rooms are currently available
* Features a whatsapp bot that can be messaged to know which rooms are currently available
* Features a telegram bot that can be messaged to know which rooms are currently available

<a name="builtwith"></a>
## Libraries
### General Libraries
* [Python](https://www.python.org/) - The core programming language
* [Flask](http://flask.pocoo.org/) - The python web development server used  
* [Jinja](http://jinja.pocoo.org/) - The template engine for Python
* [MYSQL](https://www.mysql.com/) - open source relational database used
* [MYSQL Python](https://dev.mysql.com/doc/connector-python/en/) - python database connector to MYSQL
* [Bcrypt](https://pypi.org/project/bcrypt/) - password hashing function
* [LetsEncrypt](https://letsencrypt.org/getting-started/) - to get ssl certificates for flask web application

### IOT Libraries
* [MQTT](https://docs.aws.amazon.com/iot/latest/developerguide/iot-sdks.html) - accessing AWS IoT platform through MQTT
* [MFRC522](https://github.com/mxgxw/MFRC522-python) - RFID Card Reader
* [SPI-Py](https://github.com/lthiery/SPI-Py) - sensors
* [Matrix Creator](https://matrix-io.github.io/matrix-documentation/matrix-core/getting-started/core-installation/) - used for the matrix creator

### Web Development Libraries
* [Bootstrap](https://getbootstrap.com/docs/3.3/) - CSS Framework used v3.3.7
* [JQuery](https://jquery.com/) - Simplified Javascript
* [JQuery Datatable](https://datatables.net/) - Datatable plugin for jquery
* [particle.js](https://vincentgarreau.com/particles.js/) - lightweight JavaScript library for creating particles
* [moment.js](https://momentjs.com/) - parse, validate, manipulate, and display dates and times in JavaScript.
* [HighCharts](https://www.highcharts.com/) - display interactive charts
* [animate.css](https://daneden.github.io/animate.css/) - CSS Animations
* [Noty](https://ned.im/noty/#/) - notification library
* [Font Awesome](https://fontawesome.com/icons) - used for the icons

### Bots
* [Telegram Bot](http://telepot.readthedocs.io/en/latest/) - Using telepot to leverage Telegram Bot API.
* [Discord Bot](https://github.com/Rapptz/discord.py) - Using discord.py to leverage Discord Bot API
* [Whatsapp Bot](https://www.twilio.com/docs/libraries/python) - Using Twilio's Whatsapp API using python to create an Whatsapp Bot

### Cloud Service Providers
* [AWS S3](https://aws.amazon.com/s3/) - file hosting provider for camera snapshots and motion detection videos
* [AWS EC2](https://aws.amazon.com/ec2/) - virtual machine for hosting python flask (Windows Server 2016 R2)
* [AWS IOT](https://aws.amazon.com/iot/) - broker for mqtt subscription and emission
* [AWS RDS](https://aws.amazon.com/rds/) - hosting mysql database


<a name="setup"></a>
## Setup
Run the following commands in your terminal:<br/>
Note: Does not work because this is the public repo with no keys and certs
```sh
# Download this repository
git clone https://github.com/SohWeeKiat/iot_ca2.git

# Go into the project directory
cd iot_ca2

# Install dependencies
pip install
Note: If you are unable to run this command, you have to download python 3 from  https://www.python.org/

# Run the project server
python server.py

# View the server locally
Navigate to localhost:5000
```

<a name="bot"></a>
## Bot Setup
### Discord Invite:
Link: https://discordapp.com/oauth2/authorize?client_id=545638414267973632&scope=bot&permissions=8

<img src="/Documents/images/discord_invite.PNG" alt="Telegram Invite" width="40%">

### Whatsapp Invite:
Message 'join tight-truck' to +14155238886 to access the Whatsapp Bot

<img src="/Documents/images/whatsapp_invite.jpg" alt="Whatsapp Invite" width="40%">

### Telegram Invite:
Add @wk_rpi_bot

<img src="/Documents/images/telegram_invite.jpg" alt="Telegram Invite" width="40%">

<a name="video"></a>
## Demonstration Video
* [IoT 2019 CA2 Smart Room Security](https://www.youtube.com/watch?v=WNt7YkHzFNM&t=705s)

<a name="tutorial"></a>
## Full Documentation (Including Step by Step Tutorial)
* [Word Doc](https://github.com/ThePikachu/IOT_CA2_Public/blob/master/Documents/Step%20by%20Step%20Tutorial%20(No%20Keys%20and%20Certs).docx)

<a name="authors"></a>
## Authors

* **[Soh Wee Kiat](https://github.com/SohWeeKiat)** - *Lead Developer*
* **[Samuel Chua](https://github.com/ThePikachu)** - *Assistant Developer*

See also - [Contribution History](https://github.com/SohWeeKiat/iot_ca2/contributors)

<a name="ack"></a>
## Acknowledgments

* Special Thanks for all creators of the libraries used
* Thanks to Ms Dora for the opportunity to create this project
