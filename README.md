# api

A Api foi desenvolvida para obter as dez músicas mais populares de um artista utilizando a Genius API.


#### Utilização da aplicação

Esta seção tem as etapas necessárias para a utilização da aplicação.

### Executar o projeto

1. **clone o repositório:**
  ```sh
  git clone https://github.com/denispadua/songs-api.git
  ```

2. **arquivos de ambiente:**

  Na pasta raiz do back-end `songs-api`:

  ```sh
  Altere os valores /do arquivo .env com as conexões dos servidores Amazon e o token da API Genius
  ```


3. **executando back-end:**

  Na pasta raiz do back-end `songs-api`, executar:

  ```sh
  pip install -r requirements.txt
  ```
  em seguida:
  ```sh
  flask run
  ```
## Tecnologias utilizadas

#### Back-end

- [Flask](https://flask.palletsprojects.com/en/2.1.x/)
- [AWS - DynamoDB](https://aws.amazon.com/pt/dynamodb/)
- [AWS - Redis](https://aws.amazon.com/pt/elasticache/?p=ft&c=db&z=3)

## Endpoints disponíveis

Esta seção tem como objetivo explicitar cada endpoint do projeto.

### 1. GET /api

`Parâmetros:` O usuário deverá fornecer o parâmetro artist_name=ARTIST_NAME. 
O parâmetro cache tem valor True caso nenhum valor seja informado, isso irá criar um cache no Redis.

> GET /?artist_name=xxxx

> GET /?artist_name=xxxx&cache=False