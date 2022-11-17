# Fonts Hosting

Host Google Fonts on your own server.  
With GDPR etc. using Google Fonts became a privacy compliance nightmare. So here we go.   
Either host it yourself (see below) or use my fonts hosting instance (https://fonts.angermeir.me) (also see below)

## Disclaimer
I mainly created this repository for my own website. So I might integrate minor changes on request. For big updates please fork the project and maintain it yourself :)

## General Remarks & Examples
This project only supports the latin subset in the regular variant. This is mainly due to the fact, that I couldn't figure out how to extract different variants and font versions from the google fonts URLs if not specified...

Lets look at an example:
`https://fonts.googleapis.com/css?family=Lato:400,700%7CMerriweather%7CRoboto+Mono` translates to 
- `https://<FQDN>/lato-latin-regular`
- `https://<FQDN>/merriweather-latin-regular`
- `https://<FQDN>/roboto-mono-latin-regular`

If you are a web development noob like me, you might prefer a more extensive example (taken from my website):
<details>

```
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Lato:400,700%7CMerriweather%7CRoboto+Mono&display=swap">
```

gets translated to:

```
<style>

    @font-face {
        font-family: Lato;
        font-style: normal;
        font_weight: 400;
        src: url('https://<FQDN>/lato-latin-regular.eot');
        src: local(''),
             url('https://<FQDN>/lato-latin-regular.eot?#iefix') format('embedded-opentype'),
             url('https://<FQDN>/lato-latin-regular.woff2') format('woff2'),
             url('https://<FQDN>/lato-latin-regular.woff') format('woff'),
             url('https://<FQDN>/lato-latin-regular.ttf') format('truetype'),
             url('https://<FQDN>/lato-latin-regular.svg#Lato') format('svg');
    }
    

    @font-face {
        font-family: Merriweather;
        font-style: normal;
        font_weight: 400;
        src: url('https://<FQDN>/merriweather-latin-regular.eot');
        src: local(''),
             url('https://<FQDN>/merriweather-latin-regular.eot?#iefix') format('embedded-opentype'),
             url('https://<FQDN>/merriweather-latin-regular.woff2') format('woff2'),
             url('https://<FQDN>/merriweather-latin-regular.woff') format('woff'),
             url('https://<FQDN>/merriweather-latin-regular.ttf') format('truetype'),
             url('https://<FQDN>/merriweather-latin-regular.svg#Merriweather') format('svg');
    }
    

    @font-face {
        font-family: Roboto Mono;
        font-style: normal;
        font_weight: 400;
        src: url('https://<FQDN>/roboto-mono-latin-regular.eot');
        src: local(''),
             url('https://<FQDN>/roboto-mono-latin-regular.eot?#iefix') format('embedded-opentype'),
             url('https://<FQDN>/roboto-mono-latin-regular.woff2') format('woff2'),
             url('https://<FQDN>/roboto-mono-latin-regular.woff') format('woff'),
             url('https://<FQDN>/roboto-mono-latin-regular.ttf') format('truetype'),
             url('https://<FQDN>/roboto-mono-latin-regular.svg#RobotoMono') format('svg');
    }
```

</style>
</details>

The [convert.py](convert.py) script contains the code I use to automatically remove all references and preconnects related to google fonts.

## Host it yourself
Thats pretty simple. All you need it a server running [Docker Compose](https://docs.docker.com/compose/) and a valid FQDN [Let's Encrypt](https://letsencrypt.org) can generate a TLS certificate for.
Clone the repository and insert your FQDN in `docker-compose.yml` and `nginx.tmpl` (Marked with `#TODO`). Start the containers and :rocket:


## My fonts hosting instance
- My fonts hosting instance is available via https://fonts.angermeir.me
- I will try to make it as privacy preserving as possible (e.g. no logging of IP addresses)
- If you have a website with a lot of traffic please consider to host the fonts yourself, so that my instance does not get DOSed

## Open Topics
- [ ] Entirely setup instance and configuration via terraform
- [ ] Disable logging
- [ ] Automatic build of docker container on changes
