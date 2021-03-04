# UniPi

UniPi is a WiFi voucher vending machine leveraging UniFi controller and UniFi access points. 

### Demo

[![UniPi demo](https://img.youtube.com/vi/2ENAeLyCjZY/0.jpg)](https://youtu.be/2ENAeLyCjZY)

### Pics

1. [WiFi selection](https://user-images.githubusercontent.com/13497504/99747751-1e25ca00-2b16-11eb-8bc9-caf6cbab3582.png)

2. [Voucher entry](https://user-images.githubusercontent.com/13497504/99747756-20882400-2b16-11eb-95db-4244f7b673f9.png)

3. [Finished build](https://user-images.githubusercontent.com/13497504/99747759-21b95100-2b16-11eb-9b05-f19be4b7a883.jpg)

##### Example use cases

* Single access point and a Raspberry Pi as controller server and client.
* Large deployment with wide coverage multiple access points and Raspberry Pi clients and a controller server.
* Multiple sites with cloud controller server.

##### Advantages over existing proprietary solutions

* Raspberry Pi does not handle network connections therefore no bottleneck on internet connection.
* Modular and simple for large scale sites, establishments and outdoor locations.

## Setup

### Hardware requirements

1. Raspberry Pi 3 Model B
2. Micro SD Card
3. Universal coinslot
4. Switching power supply
5. 2 pieces button switch
6. Jumper wires
7. 16x2 character LCD
8. 1 Piece 3.3k Ohms 5% resistor # for setting character LCD contrast
9. Micro USB power cable
10. UniFi wireless access point

#### Wiring

Breadboard setup

<img src="https://user-images.githubusercontent.com/13497504/99748589-c5efc780-2b17-11eb-85b9-c8f2c1126d92.png" width="600"/>

Also included `unipi.fzz` using [Fritzing](https://fritzing.org)

Finalization includes removing breadboard and connecting button and ground pins directly to the Raspberry Pi.

Connect 12V universal coinslot to BL-100 switching power supply 12V and ground.

Cut and connect Micro USB power cable to BL-100 switching power supply 5V and ground.

### Controller

Controller setup is for Raspberry Pi without a controller server existing on the network.

If you already have an existing Controller skip to [Setup Client](#setup-client).

#### Flashing Raspbian

Download Raspberry Pi OS (32-bit) Lite from [raspberrypi.org](https://www.raspberrypi.org/downloads/raspberry-pi-os/)

#### Install Docker using the convenience script

```
$ curl -fsSL https://get.docker.com -o get-docker.sh
$ sudo sh get-docker.sh

$ sudo usermod -aG docker pi

$ newgrp docker

$ sudo apt install docker-compose
```

#### Install Docker UniFi Controller for Raspberry Pi

```
$ mkdir unifi && cd unifi
$ curl -O https://raw.githubusercontent.com/ryansch/docker-unifi-rpi/master/docker-compose.yml
$ docker-compose up -d
```

Wait for a few minutes and the controller should be up at `https://raspberrypi.local:8443` or `https://<ip>:8443`

Tested on UniFi controller version 5.13.32(Build: atag_5.13.32_13646) on latest tag.

#### Configure UniFi controller (Classic settings)

##### Settings > Wireless Networks

Create Wireless Network with Name/SSD: UniPi or anything

Enable Wireless Network

Set Security as Open

##### Settings Wireless Networks > Advanced Options

Disable Block LAN to WLAN Multicast and Broadcast Data

Enable Combine 2 GHz and 5 GHz WiFi Network Names into one

##### Settings > Guest Control > Guest Policies

Enable Guest Portal
Set Authentication as Hotspot

##### Portal Customization

Customize Portal to your preference

##### Hotspot

Enable voucher-based authorization

## Setup Client

### Clone UniPi

```
$ cd ~
$ git clone https://github.com/kleo/unipi
```

### Configure config.ini

Default `config.ini` provides defaults for the client setup on the Raspberry Pi used by `unipi-coinslot`.

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

### Configure rates

Modify the script unipi-coinslot and change the set default values for upload speed allowed in kbps (optional) `up_bandwidth=4098`, download speed allowed in kbps (optional) `down_bandwidth=4098` and quantity of bytes allowed in MB (optional) `byte_quota=1000`.

More info on `create_voucher()` at [PyUnifi create_voucher](https://github.com/finish06/pyunifi#create_voucherself-number-quota-expire-up_bandwidthnone-down_bandwidthnone-byte_quotanone-notenone)

### Start UniPi client

```
$ docker-compose up -d
```

## Manual setup/development

### Install required dependencies

```
$ sudo apt install git python3-venv
```

# Setup virtual environment

```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt

$ python unipi-coinslot
```
