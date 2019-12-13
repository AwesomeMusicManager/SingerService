# SingerService
[![CircleCI](https://circleci.com/gh/AwesomeMusicManager/SingerService.svg?style=svg)](https://circleci.com/gh/AwesomeMusicManager/SingerService)

# Deployment

Serviço está de pé usando o Heroku neste [endereço](https://singer-service-app.herokuapp.com)

# Endpoints

## GET /
Endpoint para Health Check.

## GET /docs
Contém json do Swagger.

## GET /api/v1/artist

API que retorna um artista.
Contém um parâmetro:
- artist -> parâmetro obrigatório.

## GET /api/v1/lyric_check

Endpoint para realizar o Health Check do outro Microserviço que implementei, o [LyricService](https://github.com/AwesomeMusicManager/LyricService).
