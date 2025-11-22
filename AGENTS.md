# Diretrizes de Fluxo de Trabalho de IA

> **Nota para a IA:** Para obter o contexto completo sobre a visão, os objetivos e a arquitetura do sistema Caramello, consulte sempre o `README.md` e o documento detalhado em `docs/project_vision.md`.

Este projeto adota uma estratégia **DSL First** para modelagem de dados e API.
A **DSL (YAML)** é a **fonte da verdade** para a definição de entidades e estrutura do banco de dados.

## Fluxo de Trabalho Principal

1. Crie ou atualize entidades em YAML dentro da pasta `dsl/`.
2. Execute o script de geração de código: `python scripts/generate_code.py`.
3. O script irá gerar automaticamente:
   - **Modelos SQLModel** → `src/caramello/models/`
   - **Roteadores FastAPI (CRUD)** → `src/caramello/api/generated/`
4. A aplicação FastAPI (`src/caramello/main.py`) integra os roteadores gerados.
5. A documentação **OpenAPI** é gerada automaticamente pelo FastAPI em tempo de execução (`/docs`).
6. Execute e mantenha os testes em `tests/`, garantindo a integridade do sistema.

## DSL (YAML)
- O DSL é a **fonte da verdade** para descrever entidades de negócio (nome, campos, tipos, relações).
- Ele define tanto a estrutura do banco de dados (tabelas, colunas) quanto a API básica (CRUD).
- O objetivo é manter a modelagem simples e agnóstica de tecnologia.

### Convenções de Nomenclatura no DSL
- **Nome da Entidade (`name`):** Use `PascalCase` (ex: `UserProfile`), pois irá gerar uma classe Python com o mesmo nome.
- **Nome do Arquivo YAML:** Use `snake_case` (ex: `user_profile.yaml`).
- **Nome da Tabela (`table_name`):** Use `snake_case` no plural (ex: `user_profiles`).

## OpenAPI
- A **Especificação OpenAPI** é um **artefato derivado** do código (FastAPI).
- Ela serve como documentação para o frontend e clientes externos.
- Não editamos o OpenAPI manualmente; ele reflete o estado atual do código.

## Diretrizes de Idioma

O projeto adota uma estratégia de dois idiomas para equilibrar a clareza para o público-alvo e a conformidade com as práticas globais de desenvolvimento de software.

### Inglês (English)
Utilizado para toda a base de código e artefatos diretamente ligados a ela. O objetivo é manter a consistência com as ferramentas, bibliotecas e o ecossistema de programação.
- **Código-Fonte**: Nomes de arquivos, diretórios, variáveis, funções e classes.
- **Comentários e Docstrings**: Devem estar no mesmo idioma do código para evitar inconsistências.
- **Arquivos DSL (YAML)**: Todas as descrições (`description`), comentários e qualquer outro texto livre dentro dos arquivos `.yaml` na pasta `dsl/` devem estar em inglês.

### Português do Brasil (pt-BR)
Utilizado para toda a comunicação e documentação voltada para humanos. O objetivo é garantir que o projeto seja acessível e claro para a equipe e os usuários brasileiros.
- **Documentação Geral**: Conteúdo da pasta `docs/`, `README.md`, etc.
- **Mensagens de Commit**: Devem seguir o padrão em português.
- **Pull Requests**: Títulos e descrições.
- **Textos para o Usuário Final**: Mensagens de erro, interfaces e qualquer texto exibido na aplicação.

## Documentação de Referência
Regras e diretrizes adicionais estão disponíveis na pasta [`docs/`](./docs):
- [Guia de Estilo](./docs/style_guide.md)
- [Estrutura do Projeto](./docs/project_structure.md)
- [Regras de Commit](./docs/commit_rules.md)
- [Regras de Pull Request](./docs/pr_rules.md)
- [Regras de Segurança](./docs/security_rules.md)
- [Regras de Qualidade](./docs/quality_rules.md)

> **Importante:**
> - O DSL é a autoridade máxima para definição de dados.
> - O código gerado não deve ser editado manualmente (exceto se a lógica for movida para fora da geração).
> - O OpenAPI é apenas uma visualização do código.
