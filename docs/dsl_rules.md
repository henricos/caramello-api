# Regras para Criação de DSL (Caramello API)

Este documento define as regras estritas para a criação e manutenção dos arquivos de definição de entidades em `dsl/entities/*.yaml`. Estas regras devem ser seguidas por Agentes de IA e Desenvolvedores para garantir a geração correta de código.

## 1. Nomenclatura

*   **Arquivos**: Snake case (ex: `user_profile.yaml`).
*   **Entidade (`name`)**: PascalCase, singular (ex: `UserProfile`).
*   **Tabela (`table_name`)**: Snake case, **SINGULAR** (ex: `user_profile`, `family`).
    *   *Motivo*: Padronização e simplicidade em queries SQL.

## 2. Estrutura Obrigatória da Entidade

Todas as entidades (exceto tabelas de associação puras) devem conter os seguintes campos padrão:

1.  **Chave Primária Interna**:
    ```yaml
    - name: id
      type: int
      primary_key: true
      description: "Internal primary key (numeric)."
    ```
2.  **Identificador Público**:
    ```yaml
    - name: uuid
      type: UUID
      unique: true
      default_factory: uuid4
      nullable: false
      description: "Unique public identifier (UUID)."
    ```

## 3. Tipagem de Campos

Use tipos Python modernos e "lowercased" sempre que possível, exceto para classes especiais.

*   ✅ `str`, `int`, `bool`, `float`
*   ✅ `list[T]` (Python 3.10+ style)
*   ✅ `UUID` (do módulo uuid), `datetime` (do módulo datetime), `EmailStr` (do Pydantic)
*   ❌ `String`, `Integer`, `List[T]` (Typing module style antigo)

## 4. Tabelas de Associação (Link Models)

Entidades que servem apenas para conectar duas outras (Many-to-Many) devem ter a flag `is_link_model: true`.
*   Elas **NÃO** precisam de `id` ou `uuid`.
*   Devem ter duas chaves primárias compostas (Foreign Keys).

## 5. Relacionamentos

*   Use `list[EntityName]` para relacionamentos "para muitos".
*   Sempre defina `back_populates` para garantir navegação bidirecional no ORM.
*   Para Many-to-Many, especifique `link_model`.

## Exemplo Completo

```yaml
name: User
description: Represents a system user.
table_name: user  # Singular

fields:
  - name: id
    type: int
    primary_key: true
  - name: uuid
    type: UUID
    unique: true
    default_factory: uuid4
    nullable: false
  - name: tags
    type: list[str] # Lowercase generic
    nullable: true

relationships:
  - name: posts
    type: list[Post]
    back_populates: author
```
