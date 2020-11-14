## Guia para rodar o projeto com o Docker

- ### Instalação

Para o uso é necessário possuir o Docker e o Docker Compose em sua máquina.

[Instalação Docker](https://docs.docker.com/engine/installation/linux/docker-ce/)

[Instalação Docker-compose](https://docs.docker.com/compose/install/).

- ## Rodando a aplicação

Entre na pasta raíz do projeto em que está localizado o **docker-compose.yml** e digite no terminal:

&emsp;&emsp; Primeiro (Enquanto não houver alterações nas dependencias do requirements.txt ou Dockerfile, não precisará repetir o comando):

```
  docker-compose build
```

&emsp;&emsp; Em seguida use o comando para subir o ambiente com logs.

```
  docker-compose up
```

&emsp;&emsp; Espere até que o serviço esteja disponível, acesse o servidor com o seguinte endereço:

- #### https://localhost:8000


&emsp;&emsp; Após ter subido o ambiente e precisar rodar um comando dentro do novo ambiente use dessa forma:

```
  docker-compose run web <comando>
  docker-compose run web python manage.py makemigrations
```

&emsp;&emsp;&emsp; Para abrir um prompt interativo para usar quantos comandos desejar: (Para sair digite: exit)

```
 docker-compose run web sh

```
