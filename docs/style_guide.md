# Guia de Estilo Python

## Idioma

O projeto adota uma estratégia híbrida de idioma para balancear a qualidade técnica global com a agilidade de comunicação local.

### Código-Fonte e Artefatos Técnicos: Inglês (English)
Todo o código-fonte, configurações técnicas e documentação intrínseca ao código (comentários, *docstrings*) devem ser escritos em **Inglês**.
-   **Motivo:** Garante consistência com o ecossistema de desenvolvimento global (bibliotecas, frameworks), facilita a integração de ferramentas de análise estática e melhora a qualidade da geração de código por IAs, que possuem maior performance com padrões em inglês.
-   **Escopo:** Identificadores, nomes de arquivos de código, variáveis, funções, classes, módulos e pacotes.

### Documentação de Produto, Processos e Commits: Português (PT-BR)
A documentação voltada para o alinhamento do time, definição de produto (PRDs, Visão), guias de processo e mensagens de commit devem ser escritas em **Português**.
-   **Motivo:** Maximiza o entendimento mútuo entre os membros da equipe e *stakeholders*, garantindo que nuances de negócio e regras complexas sejam compreendidas sem barreiras linguísticas.

### Termos de Domínio
Termos inerentes ao contexto brasileiro (ex: `CPF`, `CNPJ`, `PIX`) são permitidos no código, mas devem ser adaptados ao estilo `snake_case` com contexto em inglês (ex: `cpf_validator`, `handle_pix_webhook`).

## Convenções de Nomenclatura
- **Pacotes/Módulos:** `snake_case` → `repositories`, `user.py`.
- **Classes:** `PascalCase` → `UserRepository`, `UserService`.
- **Funções/Variáveis:** `snake_case` → `create_user`, `max_retries`.
- **Constantes:** `UPPER_CASE` → `DEFAULT_PAGE_SIZE`.
- **Endpoints:** caminhos em `kebab-case`, funções em `snake_case`.

## Docstrings
- Siga a **PEP 257**:

```python
def create_user(data: UserCreate) -> User:
    """Creates a new user.

    Args:
        data: Validated user input data.

    Returns:
        The persisted User entity.
    """
```

## Estilo e Qualidade do Código
- **Comprimento da linha:** máx. 88 caracteres (Black).
- **Imports:** stdlib / terceiros / local (Ruff organiza).
- **Type hints:** sempre para funções públicas e objetos de domínio (verificado com mypy).
- **Ferramentas:**
  - `ruff` → lint/isort/docstyle
  - `black` → formatação
  - `mypy` → checagem de tipos
  - `pytest` → testes

## Banco de Dados
- Forneça uma `Session` por requisição via dependência (`yield`) em `database/session.py`.
- Configure o Alembic com `target_metadata = SQLModel.metadata` em `env.py`.


### Chaves Primárias e Identificadores Públicos
- **Chave Primária (PK):** Todas as tabelas devem ter uma chave primária interna do tipo `integer` autoincrementada, chamada `id`. Esta chave deve ser usada para relacionamentos (joins) entre tabelas.
- **Identificador Público:** Todas as tabelas devem ter uma coluna `uuid` do tipo `UUID`, com um valor padrão gerado e um índice `unique`. Este campo deve ser usado como o identificador público do recurso em todas as APIs externas, para evitar a exposição de IDs sequenciais.
## API
- `api/v1/routes.py`: monta os routers.
- `api/v1/users.py`: rotas de usuário.
- Use `response_model`, `status_code`, `HTTPException`.

## Repositórios e Serviços
- **Repositório:** apenas acesso a dados.
- **Serviço:** orquestração e regras de negócio.
- Nomenclatura: `UserRepository`, `UserService`.

## Testes
- `tests/` espelha a estrutura do projeto.
- Use fixtures para `Session` de banco de dados isolada.
- Hooks de pré-commit: `ruff`, `black`, `mypy`, `pytest`.
