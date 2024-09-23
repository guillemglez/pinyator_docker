# Pinyator on Docker

See https://github.com/guillemglez/Pinyator

## Dependencies
For this project, only docker-compose is required.

## Variables
The project is intended to work on its own. Anyways, it's recommended to have an own fork of the _Pinyator_ project, as the [default one](https://gitlab.com/elputorei/Pinyator) has specific configurations for _Marrecs de Salt_. As this project was done for the _Mannekes de Brusel·les_, this project refers to [this fork](https://github.com/guillemglez/pinyator).


## Build project
```bash
$ docker-compose build
$ docker-compose up -d
```

## To-Do list
[ ] Separate all the variables to a file for easier configuration
[ ] Improve README.md
