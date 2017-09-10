
# Hacks everywhere
This will be cleaned as soon as I clean up the delivery process of the blog.

# Notes:

## The **first time**:

#### On the server:
* `mkdir /static-files-webroot`
* `certbot certonly --webroot \
      -w /static-files-webroot/ \
      -d www.professionalbeginner.com \
      -d professionalbeginner.com \
      -d the-ecosystem.xyz`

#### In the `nginx.conf`:
```
## SSL Security #####################################
server {
    listen 80;

    # Redirect http->https
    location / {
      return 301 https://$host$uri;
    }

    # Serve static content
    # For cert challenge
    location /.well-known/ {
        root /static-files-webroot/;
    }
}
## END - SSL Security ###############################
```


## The *rest of the time*: **Automatic renewal**

Certificates from `letsencrypt` are only valid for 90 days.
### TODO: Document steps for automated renewal



