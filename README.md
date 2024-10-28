# Mini-Twitter Project

Um projeto Django que implementa uma plataforma estilo Twitter, permitindo que usuários façam posts, sigam uns aos outros e curtam posts.

## Requisitos

- Python 3.11
- Docker
- Docker Compose

## Estrutura do Projeto

- `docker-compose.yml`: Configuração do Docker Compose.
- `Dockerfile`: Dockerfile para construir a imagem do aplicativo.
- `requirements.txt`: Lista de dependências do Python.

## Configuração

### 1. Clonar o Repositório

Clone o repositório para a sua máquina local:

```bash
git clone https://github.com/JudsonAlex/api-minitwitter
cd api-minitwitter
```

### 2. Criar o arquivo .env

Crie um arquivo .env na raiz do projeto para armazenar suas variáveis de ambiente. Um exemplo de conteúdo:

```
DEBUG=True
DB_NAME=<NOME_DO_BANCO>
DB_USER=<USUÁRIO_DO_BANCO>
DB_PASSWORD=<SENHA_DO_BANCO>
DB_HOST=db
DB_PORT=5432
```

### 3. Construir e Executar os Containers

Para construir e iniciar os containers, execute:


```
$ docker-compose build
$ docker-compose up
```

### 5. Acessar a Aplicação

A aplicação estará disponível em http://localhost:8000.

### Executando os Testes

Para executar os testes da aplicação, você pode utilizar o seguinte comando:

bash
```
$ docker-compose exec web sh
# python3 manage.py test
```


Os testes estão organizados em aplicativos Django e cobrem as seguintes funcionalidades:

- Criação de usuários.
- Validação de autenticação.
- Funcionamento de seguir e curtir posts.

## BaseURL
http://localhost:8000/api