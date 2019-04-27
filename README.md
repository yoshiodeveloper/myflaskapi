# myflaskapi

Trabalho sobre demonstrar a utilização do Flask para criar uma API simples conectando no MongoDB.

## Instalação no Linux

> É necessário ter o Python 3, virtualenv e MongoDB instalados.

Crie um virtualenv.

```shell
$ virtualenv -p python3 venv
```

Ative o ambiente.

```shell
$ source venv/bin/activate
```

Instale as libs do Python no ambiente utilizando o arquivo "requirements.txt".

```shell
$ pip install -r requirements.txt
```

## Execução

Para iniciar a aplicação defina a variável de ambiente FLASK_ENV e execute o `flask run`.

```shell
$ export FLASK_ENV=development
$ flask run
```

> **Importante**: Esta forma de execução é apenas para o ambiente de desenvolvimento. Não deve ser executado desta forma em produção.

Agora basta abrir no navegador o site localhost:5000.

## Endpoints

É possível acessar os seguintes endpoints.

| Endpoint | Descrição |
|-|-|
| / | Exibe informações do MongoDB. |
| /<db_name> | Exibe informações de um DB específico. |
| /<db_name>/<collection_name> | Exibe informações de uma collection específica. É possível utilizar os parâmetros "limit" e/ou "skip". Exemplo: http://localhost:5000/meudb/minhacollection?skip=10&limit=20 |

Qualquer dúvida entre em contato: yoshiodeveloper@gmail.com