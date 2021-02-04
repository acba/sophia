Sophia
=======================



## Como rodar
### Em ambiente de desenvolvimento na sua máquina local

É necessário ter o virtualenv para criar um ambiente virtual do Python

```console
$ virtualvenv venv
```

Para ativar o ambiente virtual
```console
$ source venv/bin/activate
```

Instalando as dependências do projeto
```console
$ pip install -r requirements/local.txt
```

Rodando o projeto
```console
$ export $(grep -v '^#' .envs/.local/.django | xargs)
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```
