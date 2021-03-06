[![Docker Build Status](https://img.shields.io/docker/build/floriankempenich/the-gate.svg)](https://hub.docker.com/r/floriankempenich/the-gate/)

## Check the Project Page: [https://FlorianKempenich.github.io/The-Gate/](https://floriankempenich.github.io/The-Gate/)
# The Gate

### Https Front-end Proxy with Nginx & Docker
- [**Simple, secure, configurable**](#simple-secure-configurable)
- [**Usage**](#usage)
- [**Create your rules - `services.conf`**](#create-your-rules---servicesconf)
- [**Setup**](#setup)
    - [Installation](#installation)
    - [Requirements](#requirements)
- [**Configuration Examples**](#configuration-examples)
    - [Basic scenario](#basic-scenario)
    - [Certificates from Let's encrypt](#certificates-from-lets-encrypt)
- [**Extra:** Generating certificates with Let's encrypt and `certbot`](#extra-generating-certificates-with-lets-encrypt-and-certbot)

## Simple, secure, configurable

**The Gate** is a _quick to deploy_ entry gate for your server.  
It provides a **single `HTTPS` endpoint that redirects to your services.**  

**Securely serve multiple services from one single entrypoint.**
![The Gate](https://raw.githubusercontent.com/FlorianKempenich/The-Gate/master/temp/the_gate.jpg)

### No complex setup

- Just `up` and all your services are securely available.
- All the configuration is dynamically loaded, **no restart needed.**

### All services are served via `HTTPS`

- All `HTTP` connections are redirected to `HTTPS`
- Provide the certificates and they'll be loaded automatically
-    No certificates but would like to `up` **The Gate**?  
     No problem, **The Gate** generates its own self-signed certificates in case it can not find yours.  
     Your certificates will be loaded the moment they are available
-    No idea how to provide certificates?  
     Check out the dedicated section at the end: [Generating certificates with Let's encrypt and `certbot`](#extra-generating-certificates-with-lets-encrypt-and-certbot)
      
### Use your own rules

- Want to serve one service per domain? No problems!
- Want to serve different services depending on the url path? No problem!
- Be creative...

### The Gate helps you with your certificate challenges

- It serves a static directory under `www.yourdomain.com/.well-known/`
- No setup, just `up` and that directory is served.



---
## Usage

**Once the initial setup is done, start up The Gate:**

```bash
thegate up
```

You can now edit your redirection rules in the `services.conf`, and update the certificates.  
-    **Certificates:**  
     If no certificates were available at the given location, **The Gate** generates it own temporary self-signed certificates.
     Simply override them with your own, and **The Gate** will load them up. **No restart needed**.
-    **`services.conf`:**  
     Same as the certificates, **No restart needed**. Simply edit the rules, and the new rules will be reloaded.

> Before using **The Gate**: 
> - [Install](#installation) the lightweight command-line tool
> - Set up the [requirements](#requirements).
> - Create your [Rules](#create-your-rules---servicesconf)
>
> To turn The Gate off: `thegate down`


## Create your rules - `services.conf`

The main configuration of your services is in the `services.conf` file.

**This file defines:**

* All the **Services** served by `The Gate`
* The **Rules** on how to serve them

The syntax is the same as a regular `nginx` configuration file.
But only the services are defined here.

> This file will then be automatically included in the base `nginx` file.

**/!\ Each service needs to include `services.base.conf` /!\\**  
**/!\ Each service needs to include `services.base.conf` /!\\**  
**/!\ Each service needs to include `services.base.conf` /!\\**  

```nginx
server {
    include services.base.conf;

    ### REST OF THE CONFIGURATION ###
}
```

`services.base.conf` already includes everything needed for a `https` connection.
```nginx
listen 443 ssl;
ssl on;
ssl_certificate PATH_TO_YOUR_CERTIFICATE;
ssl_certificate_key PATH_TO_YOUR_PRIVKEY;
```

_**Example `services.conf` file:**_
```nginx
server {
    include services.base.conf;
    server_name professionalbeginner.com;

    location / {
        proxy_pass http://127.0.0.1:2000;
    }
}
```

See the [Configuration Examples](#configuration-examples) for more examples.

---

## Setup
### Installation
To install **The Gate**, simply run this command:
```
sudo curl -s https://raw.githubusercontent.com/FlorianKempenich/The-Gate/master/thegate -o /usr/bin/thegate && sudo chmod +x /usr/bin/thegate
```

Then **create** a configuration file at `~/.thegateconfig`.  
The configuration file is used to specify the location of the requirements on the HOST machine.

_**Example `.thegateconfig` file:**_
```
DIR_CONFIG=/https/config/
DIR_WEBROOT=/https/webroot/
DIR_CERTIFICATES=/https/letsencrypt/
FILE_CERT=./live/professionalbeginner.com/fullchain.pem
FILE_PRIVKEY=./live/professionalbeginner.com/privkey.pem
```
Read about the `.thegateconfig` different variables in the [Requirements](#requirements) section.  
See the [Configuration Examples](#configuration-examples) for more examples.

> *Note:*  
> `.thegateconfig` is the only configuration that is not reloaded on change.

> *Uninstall:*  
> The install command will download the executable for `thegate` in `/usr/bin/thegate` and make it executable.
> To remove **The Gate**: 
> ```
> sudo rm -f /usr/bin/thegate
> ```

### Requirements

**The Gate** only needs **4 elements**, for the magic to happen:

- **`Configuration directory`: The Heart of The Gate** |  `services.conf`
- **`Certificate base directory`**
- **`Certificate` & `PrivKey` file names**
- **`Webroot directory`:** From where to serve static content.

#### `Configuration directory`: The Heart of The Gate |  `services.conf`

This directory holds the most important configuration part of **The Gate: You Rules**

You **redirection rules** are configured in a file called `services.conf`. To know more about how to setup your redirections rules, check the dedicated section: [Create your rules - `services.conf`(#create-your-rules---servicesconf)  
**The `configuration directory` is the location where your `services.conf` is located on the Host machine.**

That directory will be mounted on **The Gate**, and every configuration change will be **automatically reloaded**. 
No need to restart ;)

#### Certificate base directory & Certificate/PrivKey file names
 
To serve traffic to your domains via `HTTPS` **The Gate** needs to have access to your **`SSL` certificates and private key.**

The `certificate base directory` is where these two files are located on the **Host** machine.  
The `certificate` and `private key` `filenames` are pretty self-explanatory. The `filenames` are **relative to the `certificate base directory`.**

> **Ex:**  
> If your folder structure is as follow:
> ```
> https
> └── certificates
>     ├── my_cert.pem
>     └── my_privkey.pem
> ```
> Then your configuration should be: 
> ```
> DIR_CERTIFICATES=/https/certificates
> FILE_CERT=./my_cert.pem
> FILE_PRIVKEY=./my_privkey.pem
> ```
> Another example of a valid configuration for that folder structure would be:
> ```
> DIR_CERTIFICATES=/https
> FILE_CERT=./certificates/my_cert.pem
> FILE_PRIVKEY=./certificates/my_privkey.pem
> ```

##### Special Case: Certificates as `Symlink`
In the case the `certificate` and/or `private key` `files` are actually `symlinks`, **both the `symlink` and the `actual file` must be present in the `certificate_base_dir`**

An example of that scenario is presented in the **complete configuration example: [Certificates from  Let's encrypt](#certificates-from-lets-encrypt)**


#### Webroot directory: From where to serve static content.
This folder can be _any directory_ on the host machine.  
Static content will be served under `yourdomain.com/.well-known` through `HTTP` / port `80`.
>`XXX/.well-known` is the only path accessible through `HTTP`, all other traffic is automatically redirected to `HTTPS` / port `443`

This is especially useful to host **certificates challenges from Let's encrypt / `certbot`**.  
For more information see: [Generating certificates with **Let's encrypt** and `certbot`](#extra-generating-certificates-with-lets-encrypt-and-certbot)

> **Note:**  
> Static content at the _base_ of the directory will not be accessible. 
> This is to keep the 1-1 relation between the `webroot` directory, and the `url`.  
> In other words to make a file available, say `my_file.txt`, under `yourdomain.com/.well-known/my_file.txt`: The file needs to be in a folder `.well-known` inside the `webroot` directory.
>
> ```
> webroot
> └── well-known
>     └── my_file.txt
> ```
> Additionally, a file placed at the _root_ of `webroot` will **not** be accessible.
> ```
> webroot
> ├── file_not_accessible.txt
> └── well-known
>     └── my_file.txt
> ```

---------------------------

## Configuration Examples
### Basic scenario

2 web application running on different ports.  
We want to expose each application under its own domain name.

```
- professionalbeginner.com  --REDIRECT-TO-->  Application running on port `1234`
- floriankempenich.com      --REDIRECT-TO-->  Application running on port `8888`
```

Certficates are static and stored in the same folder.

#### Folder structure
```
https
├── certificates
│   ├── my_certificate.pem
│   └── my_private_key.pem
├── servicesconfig
│   └── services.conf
└── webroot
```


#### `.thegateconfig`
```
DIR_CONFIG=/https/servicesconfig/
DIR_WEBROOT=/https/webroot/
DIR_CERTIFICATES=/https/certificates/
FILE_CERT=my_certificate.pem
FILE_PRIVKEY=my_private_key.pem
```

#### `services.conf`
```nginx
server {
    include services.base.conf;
    server_name professionalbeginner.com;

    location / {
        proxy_pass http://127.0.0.1:1234;
    }
}

server {
    include services.base.conf;
    server_name floriankempenich.com;

    location / {
        proxy_pass http://127.0.0.1:8888;
    }
}
```


### Certificates from Let's encrypt 

In this scenario, only one web app is running.  
We want to expose it using **certificates generated by Let's encrypt.**

```
professionalbeginner.com  --REDIRECT-TO-->  Application running on port `1234`
```


#### Folder structure

Certificates from **Let's encrypt** need to be renewed every 90 days.  
To facilitate that, **Let's encrypt** uses a particular folder structure and certificates are accessed through `symlinks`.

>**Let's encrypt folder structure:**
```
/etc/letsencrypt
├── accounts
│   └── acme-v01.api.letsencrypt.org
│       └── directory
│           └── cb3660c15be23b89e048d04b0530379e
│               ├── meta.json
│               ├── private_key.json
│               └── regr.json
├── archive
│   └── professionalbeginner.com
│       ├── cert1.pem
│       ├── chain1.pem
│       ├── fullchain1.pem
│       └── privkey1.pem
├── csr
│   └── 0000_csr-certbot.pem
├── keys
│   └── 0000_key-certbot.pem
├── live
│   └── professionalbeginner.com
│       ├── cert.pem -> ../../archive/professionalbeginner.com/cert1.pem
│       ├── chain.pem -> ../../archive/professionalbeginner.com/chain1.pem
│       ├── fullchain.pem -> ../../archive/professionalbeginner.com/fullchain1.pem
│       ├── privkey.pem -> ../../archive/professionalbeginner.com/privkey1.pem
│       └── README
└── renewal
    └── professionalbeginner.com.conf
```

This folder configuration can totally be in a different folder than our **Webroot** and **Service configuration** folders.
```
/thegate
├── servicesconfig
│   └── services.conf
└── webroot

/etc/letsencrypt
|...
```


#### `.thegateconfig`
> Remember, the only constraint when using `symlink`. Both the `symlink` **and** the `file` must be contained in the `DIR_CERTIFICATES` base directory.

```
DIR_CONFIG=/thegate/servicesconfig/
DIR_WEBROOT=/thegate/webroot/
DIR_CERTIFICATES=/etc/letsencrypt/
FILE_CERT=./live/professionalbeginner.com/fullchain.pem
FILE_PRIVKEY=./live/professionalbeginner.com/privkey.pem
```

#### `services.conf`
```nginx
server {
    include services.base.conf;
    server_name professionalbeginner.com;

    location / {
        proxy_pass http://127.0.0.1:1234;
    }
}
```

## Extra: Generating certificates with **Let's encrypt** and `certbot`

Using **Let's encrypt** and `certbot` it is super easy to get **free `SSL` certificates**.  
There are multiple ways to use `certbot`, the tool used to request these certificates, but thanks to **The Gate** it is now easier than ever.

**Six simple steps**:

1.    **Configure the location where the certificates _will_ be stored**.  
      By default certificates are stored under `/etc/letsencrypt/live/YOURDOMAIN/`, and are `symlink` to files located in `/etc/letsencrypt/archive/YOURDOMAIN/`  
      The filenames are `fullchain.pem` and `privkey.pem` for the certificates and private key respectively.  
      **_A correct `.thegateconfig` would be:_**
      ```
      DIR_CERTIFICATES=/etc/letsencrypt/
      FILE_CERT=./live/YOURDOMAIN/fullchain.pem
      FILE_PRIVKEY=./live/YOURDOMAIN/privkey.pem


      # Also set the rest of the configuration
      # DIR_CONFIG=Where `service.conf` is located
      # DIR_WEBROOT=Webroot directory
      ```
      > Read more about it in the [Let's Encrypt folder structure section](#folder-structure-1) and on the [official website of the `certbot` tool](https://certbot.eff.org/docs/using.html#where-are-my-certificates)

2.    **Start up The Gate**  
      ```
      thegate up
      ```
      **The Gate** will start serving your services, thanks to a self-signed auto-generated certificate. 
      But more importantly, **The Gate** will serve static content on the `DIR_WEBROOT`.  
      The `DIR_WEBROOT` will be used by `certbot` to place the certificates challenges.

3.    **Delete the temporary certificates**  
      To have a service up and running as quick as possible, **The Gate** generates its own self-signed certificates if it cannot find existing ones.  
      **Before generating new certificates, we need to delete the existing ones.**
      ```
      rm -rf /etc/letsencrypt/live/YOURDOMAIN
      ```
      > If not, when noticing an existing directory, `certbot` will assume the certificates already exist for this domain and skip the generation.

      
4.    **Install `certbot`**
       ```
       sudo apt-get update
       sudo apt-get install software-properties-common
       sudo add-apt-repository ppa:certbot/certbot
       sudo apt-get update
       sudo apt-get install certbot 
       ```
5.    **Run `certbot` using the `webroot` plugin**
      ```
      sudo certbot certonly --webroot \
           -w DIR_WEBROOT \
           -d professionalbeginner.com \
           -d www.professionalbeginner.com \
           -d anotherdomain.net

      ```
      > `DIR_WEBROOT` is the directory to **The Gate** in `.thegateconfig`.  
      > Read more about the webroot directory in the dedicated section: [Webroot directory: From where to serve static content.](#webroot-directory-from-where-to-serve-static-content)
6.    **Set a `cron` job to automatically renew the certificates**  
      Add a `cron` or `systemd` job which runs the following:  
      ```
      certbot renew
      ``` 
7.    **Enjoy `HTTPS`**  
      After the certificate generation was completed in step 3, **The Gate** automatically reloaded the new certificates. Also each time the certificates will be renewed, they will be automatically reloaded by **The Gate**.

**You can now access your domains through `HTTPS`** 


To learn more about `certbot` and **Let's encrypt**, head over to their website:
- [https://certbot.eff.org/](https://certbot.eff.org/)
- [https://letsencrypt.org/](https://letsencrypt.org/)

