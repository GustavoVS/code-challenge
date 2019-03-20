# code-challenge-backend

Solução utilizando [Python 3](https://www.python.org/downloads/) e o framework [Django 2.1](https://www.djangoproject.com/) para o code-challenge: https://github.com/ZXVentures/code-challenge/blob/master/backend.md

## Executando localmente

Antes de começar, é necessário ter instalado no Sistema Operacional os programas Python, PostgreSQL e PostGIS. 
Links para instalação:

- [Python](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/)
- [PostGIS](https://postgis.net/install/)

### Banco de dados
É necessário que o banco de dados tenha a extensão `postgis`, para isso será necessário que o usuário que acessa o banco seja `superuser` ou que a extensão seja adicionada posteriormente utilizando o usuário `postgres`.

IMPORTANTE: os seguintes comandos são para sistema Linux. Se estiver utilizando outro sistema operacional, será necessário utilizar o comando equivalente.
#### Criando o usuário
Com o usuário `postgres`crie a role no banco de dados para o seu usuário, neste exemplo será o usuário "pdvs".

```
$ sudo su - postgres -c "createuser -d pdvs"
```
Para tornar o usuário `superuser` (para adicionar a extensão `postgis`automaticamente) é necessário o seguinte comando:
```
$ sudo su - postgres -c "psql -c 'ALTER USER pdvs WITH SUPERUSER;'"
```

#### Criando o banco
Por padrão, a aplicação tentará acessar o banco chamado `pdvs`. Caso deseje utilizar outro nome será necessário alterar no projeto o arquivo `settings.py`.
```
$ createdb pdvs
```
Se o seu usuário não for superuser, será necessário adicionar o `postgis` ao banco manualmente com o seguinte comando:

```
$ sudo su - postgres -c "psql pdvs -c 'CREATE EXTENSION postgis;'"
```

### Executando a aplicação
É aconselhável utilizar o [Virtualenv](https://virtualenv.pypa.io/en/latest/installation/) para instalar os packages da aplicação e não no sistema operacional.

Crie e ative seu virtualenv com o seguinte comando:
```
$ virtualenv env
$ source env/bin/activate
```
Da raíz do projeto (`code_challenge_backend/`, utilize o pip para instalar as dependências:
```
$ pip install -r requirements.txt
```
Sincronize o banco de dados:

```
$ python manage.py migrate
```
Execute a aplicação
```
$ python manage.py runserver
```
Após isso, basta acessar os métodos através da url http://localhost:8000

### Métodos

- Para criar um PDV, é necessário utilizar o método `POST`, enviando os dados no endpoint `api/pdv`
- Para recuperar um PDV, basta colocar o `id` do PDV no endpoint`api/pdv/[id]`. Exemplo: http://localhost:8000/api/pdv/7/
- Para pesquisar o PDV mais próximo de uma `lat` e `lng`, a `lat`e a `lng` são passadas através de parâmetros no endpoint `api/search-pdv/?lat=[lat]&lng=[lng]`.  Exemplo: http://localhost:8000/api/search-pdv/?lat=-23.6823&lng=-46.6298
