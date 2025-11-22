# Caramello Backend

Serviços backend para o sistema pessoal de organização familiar Caramello.

## Índice

- [Sobre](#sobre)
- [Funcionalidades](#funcionalidades)
- [Instalação](#instalação)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Tecnologias](#tecnologias)
- [Contribuição](#contribuição)
- [Licença](#licença)
- [Links Relacionados](#links-relacionados)
- [Contato](#contato)

## Sobre

O Caramello é um sistema pessoal e integrado para organização familiar. Este repositório contém os serviços backend (a API) escritos em Python, que servem como a base para todas as aplicações do ecossistema Caramello (web e mobile).

O objetivo do projeto é centralizar diversas ferramentas de uso individual e compartilhado, como agenda, finanças, listas de compras, saúde e entretenimento, para simplificar a gestão do dia a dia da família.

Para uma descrição detalhada da visão e de todas as funcionalidades planejadas, consulte o documento [Visão do Projeto](./docs/project_vision.md).

## Funcionalidades

O Caramello visa oferecer um conjunto diversificado de ferramentas para a gestão familiar. Algumas das principais funcionalidades planejadas incluem:

-   **Agenda Familiar**: Compromissos individuais e compartilhados.
-   **Gestão de Compras**: Lista de compras colaborativa em tempo real.
-   **Controle de Despensa**: Inventário de itens domésticos.
-   **Entretenimento**: Listas de filmes, séries e livros.
-   **Finanças Pessoais**: Controle de gastos e orçamento familiar.
-   **Saúde da Família**: Histórico médico e controle de medicação.
-   **Tarefas e Lembretes**: Organização de responsabilidades diárias.

Para uma descrição detalhada da visão e de todas as funcionalidades planejadas, consulte o documento [Visão do Projeto](./docs/project_vision.md).

## Instalação

Para configurar o ambiente de desenvolvimento e instalar as dependências do projeto, você precisará do `uv`.

1.  **Instale o `uv` (se ainda não tiver):**
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

2.  **Crie o ambiente virtual:**
    ```bash
    uv venv
    ```

    **Ative o ambiente virtual:**
    ```bash
    source .venv/bin/activate
    ```

3.  **Instale as dependências do projeto:**
    ```bash
    uv pip install -e .
    ```

4.  **Instale as dependências de desenvolvimento (para geração de código):**
    ```bash
    uv pip install ".[dev]"
    ```

## Uso

O projeto Caramello Backend utiliza um fluxo de trabalho onde DSLs em YAML definem as entidades. Um script de geração cria automaticamente os modelos SQLModel e os roteadores FastAPI, que por sua vez servem de base para a geração automática de migrações de banco de dados (Alembic).

### Geração de Código

O script de geração está localizado na pasta `scripts/`. Certifique-se de que seu ambiente virtual esteja configurado e as dependências de desenvolvimento instaladas antes de executar.

1.  **Gerar Modelos e API a partir do DSL:**
    Este script lê as definições de entidade em `dsl/entities/` (conforme listado em `dsl/manifest.yaml`) e gera os modelos em `src/caramello/models/` e os roteadores em `src/caramello/api/generated/`.
    ```bash
    uv run python scripts/generate_code.py
    ```

### Migrações de Banco de Dados (Alembic)

Após gerar os novos modelos, você deve criar e aplicar as migrações para atualizar o banco de dados.

1.  **Gerar Script de Migração:**
    O Alembic detectará as mudanças nos modelos gerados e criará um arquivo de revisão.
    ```bash
    uv run alembic revision --autogenerate -m "descricao_da_mudanca"
    ```

2.  **Aplicar Migrações:**
    Atualize o banco de dados para a versão mais recente.
    ```bash
    uv run alembic upgrade head
    ```

## Estrutura do Projeto

### Pastas principais:

-   **`alembic/`**: Scripts de migração de banco de dados (Alembic).
-   **`docs/`**: Documentação detalhada do projeto.
-   **`dsl/`**: Definições de objetos de domínio em YAML (DSL). Gera código e OpenAPI.
-   **`src/caramello/`**: Pacote principal da aplicação.
    -   **`api/`**: Routers FastAPI (endpoints).
    -   **`core/`**: Configurações globais, variáveis de ambiente, utilitários.
    -   **`database/`**: Conexão com o banco de dados e configuração de sessão.
    -   **`models/`**: Modelos SQLModel (tabelas do banco de dados).
    -   **`repositories/`**: Camada de acesso a dados (queries).
    -   **`schemas/`**: Schemas Pydantic para validação.
    -   **`services/`**: Camada de lógica de negócio.
-   **`tests/`**: Testes automatizados.

## Tecnologias

O projeto é construído sobre uma stack moderna de Python:

-   **Python 3.10+**
-   **FastAPI**: Framework web moderno e de alta performance.
-   **SQLModel**: ORM que combina SQLAlchemy e Pydantic.
-   **Alembic**: Ferramenta de migração de banco de dados.
-   **Pydantic**: Validação de dados e gerenciamento de configurações.
-   **uv**: Gerenciador de pacotes e projetos Python extremamente rápido.

## Contribuição

Este projeto é pessoal, mas você pode usar esta seção para registrar como planejar melhorias, usar IA, etc.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Links Relacionados

- [Caramello Backend](https://github.com/henricos/caramello-backend)
- [Caramello Frontend Web](https://github.com/henricos/caramello-frontend-web)
- [Caramello Mobile](https://github.com/henricos/caramello-mobile)

## Contato

[Henrico Scaranello](https://github.com/henricos)
