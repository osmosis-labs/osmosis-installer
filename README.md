#Bash Installer
Simple installer with the following features:

TODO: ADD INSTRUCTIONS HERE.

# Web Server
Simple docker web server used to serve the bash file used to download the installer. 

## Setup
Setup a DigitalOcean Docker server, or setup your own.

#### Build Image

You need to run if you modify anything on the Dockerfile
```
docker build -t simple-nginx .
```

#### Run Image

```
docker run -d -it -p 80:80 simple-nginx
```

#### See running process

``` 
docker ps
```

#### Kill Server where {CONTAINER ID} was obtained from docker ps

``` 
docker kill {CONTAINER ID}
```

####  DNS Entries
Add a dns entry to Cloudflare to point to your droplet's IP address

### Access the installer via the domain name such

```bash
curl https://get.osmosis.zone/installer.bash | sudo bash
```
