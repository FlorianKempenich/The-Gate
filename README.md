# The Gate

### Https Front-end Proxy with Nginx & Docker

## Simple, secure, configurable

**The Gate** is a _quick to deploy_ entry gate for your server.  
It provides a **single `HTTPS` endpoint that redirects to your services.**  

**Securely serve multiple services from one single entrypoint.**
![The Gate](https://gitlab.com/the_gate/the_gate/raw/master/temp/the_gate.jpg)

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
     [The Gate - Certificate Daemon](https://gitlab.com/the_gate/the_gate_certificate_daemon) does that for you ;)
      
### Use your own rules

- Want to serve one service per domain? No problems!
- Want to serve different services depending on the url path? No problem!
- Be creative...

### The Gate helps you with your certificate challenges

- It serves a static directory under `www.yourdomain.com/.well-knows/`
- No setup, just `up` and that directory is served.



---
## Usage

**Once the initial setup is done, start up The Gate:**

```bash
thegate up
```

**All configuration is loaded dynamically, no need to restart between each change.**  


> Before using **The Gate**: 
> - [Install](#Installation) the lightweight command-line tool
> - Set up the [requirements](#Requirements).
>
> To turn The Gate off: `thegate down`

---

### Installation

To install **The Gate**, simply run this command:
```
sudo curl -s https://gitlab.com/the_gate/the_gate/raw/master/thegate -o /usr/bin/thegate && sudo chmod +x /usr/bin/thegate
```

Then **create** a configuration file at `~/.thegateconfig`.  
The configuration file is used to specify the location of the requirements on the HOST machine.

*Example `.thegateconfig` file:*
```
DIR_CONFIG=/https/config/
DIR_WEBROOT=/https/webroot/
DIR_CERTIFICATES=/https/letsencrypt/
FILE_CERT=./live/professionalbeginner/fullchain.pem
FILE_PRIVKEY=./live/professionalbeginner/privkey.pem
```
Read about the `.thegateconfig` different variables in the [Requirements](#Requirements) section.

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

You **redirection rules** are configured in a file called `services.conf`. To know more about how to setup your redirections rules, check the dedicated section: [Create your own rules | `services.conf`](#create-your-own-rules--servicesconf)  
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

An example of that scenario is presented in the **complete configuration example:**  
**[An Example: Using Let's encrypt]()**

#### Webroot directory: From where to serve static content.
Describe quickly
And explain how it works in term of "what path the directory actually serves"
--> Remember that we can not serve the `root` directly under well known, because that is not expected by let's encrypt
The basic explanation is:

Everything under `YOUR_STATIC_DIRECTORY/.well-known/` will be served under `http://www.yourdomain.com/.well-knows/`
--> Port 80, no https for this one.

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- The Gate
    - -
    - Simple, secure, configurable
        - No complex setup
        - All services are served via `HTTPS`
        - Use your own rules
        - The Gate helps with your certificate challenges
    - Usage
        - `thegate up`
        - Installation
        - Requirements
            - `Configuration directory`: The Heart of The Gate |  `services.conf`
            - Certificate base directory & Certificate/PrivKey file names
                - Special Case: Certificates as `Symlink`
            - Webroot directory: From where to serve static content.
        - Create your own rules | `services.conf`
        - Examples
            - Service:
            - Complete configuration
    - Configuration Examples

<!-- markdown-toc end -->



### Create your own rules | `services.conf`

The main configuration of your services is in the `services.conf` file.

**This file defines:**

* All the **Services** served by `The Gate`
* The **Rules** on how to serve them

The syntax is the same as a regular `nginx` configuration file.
But only the services are defined here.
This file will then be included in the General `nginx` file.

**/!\ Each service needs to include `services.base.conf` /!\\**  
**/!\ Each service needs to include `services.base.conf` /!\\**  
**/!\ Each service needs to include `services.base.conf` /!\\**  

    server {
        include services.base.conf;

        // REST OF THE CONFIGURATION
    }

`services.base.conf` already includes everything needed for a `https` connection.

    listen 443 ssl;
    ssl on;
    ssl_certificate PATH_TO_CERTIFICATES/fullchain.pem;
    ssl_certificate_key PATH_TO_CERTIFICATES/privkey.pem;

### Examples
#### Service:

    server {
        include services.base.conf;
        server_name professionalbeginner.com;

        location / {
            proxy_pass http://127.0.0.1:2000;
        }
    }

#### Complete configuration
An example of a working `services.conf` is available in the repository.



---------------------------------------------
## Configuration Examples



















---------------------------------------------
# OLD  OLD OLD OLD OLD OLD OLD OLD OLD OLD OLD OLD OLD OLD OLD OLD OLD OLD OLD OLD OLD OLD OLD OLD OLD
# Nginx as a Front-End Proxy

This project offers a out of the box pre-configured `nginx` server running in a docker image.
Simply customise the `nginx.conf` to redirect to the correct services


## Usage
- Customise the `nginx.conf`
- Run `docker-compose up --build -d`

To stop the `nginx`: `docker-compose down`


# TODO
# TODO
## Make explicit that this is specifically targeted for 1 use case:
### Certificates Generated by `Letsencrypt`
### One certificate for all domains served by this `nginx`
# TODO
# TODO


## Use HTTPS

It is possible and very simple to use `HTTPS` thanks to this project:
- [Certificate generation project](https://gitlab.com/the_blog/letsencrypt-docker-daemon)

### Initial setup
As explained in the `README.md` of the [certificate generation project](https://gitlab.com/the_blog/letsencrypt-docker-daemon).
We need to serve static content.

**To do so:**
- Create a directory.
  - For example in `/https/webroot`
- Serve this directory under `DOMAIN/.well-known/`
  - In the `nginx.conf`:
  ```
    ## SSL Security #####################################
    server {
        listen 80;

        # Serve static content (for the certificate challenge)
        location /.well-known/ {
            root /https/webroot/;
        }
    }
    ## END - SSL Security ###############################
  ```

### Generate the certificate & auto-renew
Follow the instructions on the [certificate generation project](https://gitlab.com/the_blog/letsencrypt-docker-daemon).

 
