# API Medical Control
<span>
    <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"/>
    <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi"/>
    <img src="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white"/>
    <img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white"/>
    <img src="https://img.shields.io/badge/GoogleCloud-%234285F4.svg?style=for-the-badge&logo=google-cloud&logoColor=white"/>
</span>


# Blog API

Esta é uma API desenvolvida com FastAPI para gerenciar um blog. A API oferece um conjunto completo de funcionalidades CRUD (Criar, Ler, Atualizar, Deletar) para posts de blog, além de autenticação de usuários e paginação de dados.

## Funcionalidades

- **Gerenciamento de Posts**: Criação, leitura, atualização e exclusão de posts de blog.
- **Autenticação**: Sistema de login e registro de usuários com segurança.
- **Paginação**: Facilita a navegação em listas extensas de posts.
- **Documentação Automática**: Interface gerada automaticamente para explorar a API.

## Tecnologias

- **FastAPI**: Framework principal para construção da API.
- **SQLAlchemy**: ORM utilizado para interagir com o banco de dados.
- **Pydantic**: Utilizado para validação e definição de schemas.
- **JWT**: Implementação de autenticação com tokens JWT.

## Como Rodar a Aplicação

1. Clone o repositório:
    ```bash
    git clone https://github.com/JoaoNogueira23/api-blog.git
    ```
2. Depedências
    ```
    docker, veja em https://www.docker.com/
    poetry (pip install poetry)
    ```
3. Construção da Imagem (Docker)
    ```bash
    docker-compose up -d
    ```
3. Configuração do Ambiente (windows):
    ```bash
    poetry shell
    poetry install
    poetry run uvicorn main:app --port 8080 --reload
    ```
4. Configure as variáveis de ambiente no arquivo `.env`.
    ```bash
    PG_USER='admin'
    PG_PASS='admin123'
    PG_DB='db_agency'
    DATABASE_UREL='postgresql+asyncpg://admin:admin123@localhost:5432/db_agency
    ```
5. Execute a aplicação:
    ```bash
    poetry run uvicorn main:app --port 8080 --reload
    ```

## Documentação da API

A documentação interativa da API pode ser acessada em `http://localhost:8000/docs` após rodar a aplicação.

## Contribuição

Sinta-se à vontade para contribuir com melhorias! Envie um pull request ou abra uma issue para discutirmos as mudanças.

## Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.


