# Setup

# Install required dependencies

```
$ sudo apt install git python3-venv
```

# Controller

Controller setup is for Raspberry Pi setups without a Controller server existing on the network. 

If you already have an existing Controller skip to [Setup virtual environment](#setup-virtual-environment).

## Install Docker using the convenience script

```
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

sudo usermod -aG docker pi

sudo apt install docker-compose
```

## Install Unifi Docker Controller for Raspberry Pi 2/3

```
$ mkdir unifi && cd unifi
$ curl -O https://raw.githubusercontent.com/ryansch/docker-unifi-rpi/master/docker-compose.yml
$ sudo docker-compose up -d
```

Wait for a few minutes and the controller should be up at https://raspberrypi.local:8443

# Setup virtual environment

```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

# Configure config.ini

Default config.ini provides defaults for the Controller setup on the Raspberry Pi.

Example config.ini

```
[config]
# the controller address (default "unifi", example "unifi.example.com")
controller 	= localhost
# the controller username (default "admin")
username 	= admin
# the controller password
password 	= password
# the controller port (default "8443")
port 		= 8443
# the controller base version (default "v5")
version 	= v5 
# the site ID, UniFi >=3.x only (default "default")
siteid 		= default
# don't verify ssl certificates set as True or False without quotes
nosslverify = True
# verify with ssl certificate pem file (not required)
certificate =  
```


