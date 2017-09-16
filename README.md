
## Requirements
- 1 folder to serve static content
- 1 folder where certificates are stored, or will be stored
- Services configuration

## Services configuration

The main configuration of your services is in the `services.conf` file.

**This file defines:**

* All the **Services** served by `The Gate`
* The **Rules** on how to serve them

The syntax is the same as a regular `nginx` configuration file.
But only the services are defined here.
This file will then be included in the General `nginx` file.

**Each service needs to include `services.base.conf`**

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
An example of a working `services.conf` is available under `services.conf.template`
























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

