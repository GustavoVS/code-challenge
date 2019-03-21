# code-challenge-backend

Solução utilizando [Python 3](https://www.python.org/downloads/) e o framework [Django 2.1](https://www.djangoproject.com/) para o code-challenge: https://github.com/ZXVentures/code-challenge/blob/master/backend.md

## Executar localmente

Para executar localmente é necessário ter instalado o [Docker](https://docs.docker.com/install/) e o [Docker Compose](https://docs.docker.com/compose/install/).
Com o Docker Compose instalado, basta acessar o diretório do projeto `code_challenge_backend` e executar o comando:
```
$ docker-compose up
```
Após isso a aplicação será executada em http://localhost:8000.

## Métodos

- Para criar um PDV, é necessário utilizar o método `POST`, enviando os dados no endpoint `api/pdv`
- Para recuperar um PDV, basta colocar o `id` do PDV no endpoint`api/pdv/[id]`. Exemplo: http://localhost:8000/api/pdv/7/
- Para pesquisar o PDV mais próximo de uma `lat` e `lng`, a `lat`e a `lng` são passadas através de parâmetros no endpoint `api/search-pdv/?lat=[lat]&lng=[lng]`.  Exemplo: http://localhost:8000/api/search-pdv/?lat=-23.6823&lng=-46.6298
