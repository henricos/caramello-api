# Contexto e Diretrizes para Agentes IA

> **Contexto Crítico:** Este projeto (`caramello-api`) é o backend Python/FastAPI do ecossistema Caramello. Antes de começar, entenda a [Visão do Projeto](./docs/project_vision.md) e o [README](./README.md).

## 1. Princípios Fundamentais (DSL First)
Este projeto **NÃO** segue o fluxo tradicional de criar models/routers manualmente.
- **Fonte da Verdade**: Arquivos YAML em `dsl/`.
- **Fluxo**: Editar YAML -> Rodar `generate_code` -> Validar.
- **Proibido**: Editar arquivos em `src/caramello/models` ou `src/caramello/api/generated` manualmente. Eles serão sobrescritos.

## 2. Stack Tecnológica
- **Gerenciador**: `uv`
- **Framework**: FastAPI (Async)
- **ORM**: SQLModel / SQLAlchemy (Async)
- **Migrações**: Alembic
- **Banco**: PostgreSQL (Obrigatório em Dev e Prod).

## 3. Comandos Operacionais (Cheat Sheet)
Para evitar alucinações sobre como rodar o projeto e garantir agilidade:

### 🚀 Rodar Aplicação
```bash
# Sobe servidor de desenvolvimento na porta 8000 com reload
uv run uvicorn caramello.main:app --reload
```

### 🧪 Rodar Testes
```bash
# Executa todos os testes
uv run pytest
```

### 🛠️ Comandos de Manutenção (bin/)
| ID | Comando | Descrição |
| :--- | :--- | :--- |
| **Gen** | `./bin/generate_code` | Gera Models, Routers e Testes a partir do DSL. |
| **Migrate** | `alembic revision --autogenerate` | Cria migração baseada nos models gerados. |
| **DB** | `./bin/manage_db` | Gerencia o banco (init, migrate, upgrade). |
| **Check** | `./bin/validate_generation` | Verifica consistência e roda testes gerados. |

## 4. Diretrizes de Idioma
Consulte [docs/language_rules.md](./docs/language_rules.md) para a política completa.

| Contexto | Idioma | Exemplo |
| :--- | :--- | :--- |
| **Código/DSL** | Inglês | `class UserProfile`, `def get_user`, `user_profiles.yaml` |
| **Documentação** | Português (BR) | `README.md`, docstrings, comentários, commits |
| **Commits** | Português (BR) | `feat: adiciona nova entidade de perfil` |
| **PRs** | Português (BR) | Título e descrição em PT-BR |

## 5. O que NÃO Fazer (Restrições)
1.  **NUNCA edite código gerado.** Se precisar alterar um Model, edite o YAML.
2.  **NUNCA crie arquivos `.env` sem permissão.** Use as variáveis de ambiente baseadas no `.env.example`.
3.  **NUNCA altere a estrutura de pastas** sem consultar a seção "Estrutura do Projeto" no `README.md`.

## 6. Documentação Detalhada
Para detalhes profundos que não cabem aqui:
- **Idioma**: [`docs/language_rules.md`](./docs/language_rules.md)
- **Estilo de Código**: [`docs/style_guide.md`](./docs/style_guide.md)
- **Estrutura**: [`README.md`](./README.md#estrutura-do-projeto)
- **Qualidade**: [`docs/quality_rules.md`](./docs/quality_rules.md)
- **Segurança**: [`docs/security_rules.md`](./docs/security_rules.md)
- **Regras de Commit**: [`docs/commit_rules.md`](./docs/commit_rules.md)
