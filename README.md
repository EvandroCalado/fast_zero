# Todo App FastAPI

**Todo App** é um aplicativo TODO desenvolvido como parte de um curso sobre FastAPI. Este projeto demonstra como construir uma API RESTful utilizando FastAPI, SQLAlchemy e outras bibliotecas populares do ecossistema Python.

## Tecnologias Utilizadas

- **FastAPI**: Um moderno framework web para construção de APIs com Python 3.7+ baseado em tipos de dados.
- **SQLAlchemy**: Um ORM (Object Relational Mapper) para interação com o banco de dados.
- **Alembic**: Uma ferramenta de migração de banco de dados para SQLAlchemy.
- **Pydantic**: Validação de dados usando modelos de dados.
- **JWT (JSON Web Tokens)**: Para autenticação.
- **PostgreSQL**: Sistema de gerenciamento de banco de dados.

## Instalação

Para instalar as dependências do projeto, utilize o **Poetry**. Certifique-se de que você tem o Poetry instalado em seu sistema. Siga os passos abaixo:

1. Clone o repositório:
   ```bash
   git clone git@github.com:EvandroCalado/fast_zero.git
   cd fast-zero
   ```

2. Instale as dependências:
   ```bash
   poetry install
   ```

3. Ative o ambiente virtual:
   ```bash
   poetry shell
   ```

## Executando o Projeto

Para iniciar o servidor FastAPI, utilize o comando:

```bash
task dev
```

O servidor estará disponível em `http://localhost:8000`. Você pode acessar a documentação da API em `http://localhost:8000/docs`.

## Executando Testes

Para executar os testes do projeto, utilize o seguinte comando:

```bash
task test
```

Os testes são realizados com **pytest** e os resultados de cobertura são gerados.

## Linting e Formatação

Para garantir a qualidade do código, utilize o comando:

```bash
task lint
```

E para formatar o código, utilize:

```bash
task format
```

## Estrutura do Projeto

```plaintext
fast-zero/
│
├── fast_zero/
│   ├── __init__.py
│   ├── app.py               # Arquivo principal da aplicação FastAPI
│   ├── models.py            # Modelos de dados usando SQLAlchemy
│   ├── schemas.py           # Schemas de validação usando Pydantic
│   ├── database.py          # Configuração do banco de dados
│   ├── routes.py            # Rotas da API
│   └── services.py          # Lógica de negócios
│
├── alembic/                 # Diretório para migrações do Alembic
│
├── tests/                   # Diretório para testes
│   ├── __init__.py
│   └── test_app.py          # Testes da aplicação
│
├── pyproject.toml           # Configurações do projeto
├── README.md                # Este arquivo
└── .gitignore               # Arquivo para ignorar arquivos no Git
```

## Contribuição

Se você deseja contribuir para este projeto, sinta-se à vontade para fazer um fork e enviar pull requests.

## Licença

Este projeto é licenciado sob a MIT License. Veja o arquivo `LICENSE` para mais detalhes.

## Autor

**Evandro Calado**  
[evandrocalado07@gmail.com](mailto:evandrocalado07@gmail.com)

