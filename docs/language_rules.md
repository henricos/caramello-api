# Diretrizes de Idioma

O projeto adota uma estratégia híbrida de idioma para balancear a qualidade técnica global com a agilidade de comunicação local.

## Código-Fonte e Artefatos Técnicos: Inglês (English)
Todo o código-fonte, configurações técnicas e documentação intrínseca ao código (comentários, *docstrings*) devem ser escritos em **Inglês**.
-   **Motivo:** Garante consistência com o ecossistema de desenvolvimento global (bibliotecas, frameworks), facilita a integração de ferramentas de análise estática e melhora a qualidade da geração de código por IAs, que possuem maior performance com padrões em inglês.
-   **Escopo:** Identificadores, nomes de arquivos de código, variáveis, funções, classes, módulos e pacotes.

## Documentação de Produto, Processos e Commits: Português (PT-BR)
A documentação voltada para o alinhamento do time, definição de produto (PRDs, Visão), guias de processo e mensagens de commit devem ser escritas em **Português**.
-   **Motivo:** Maximiza o entendimento mútuo entre os membros da equipe e *stakeholders*, garantindo que nuances de negócio e regras complexas sejam compreendidas sem barreiras linguísticas.

## Termos de Domínio
Termos inerentes ao contexto brasileiro (ex: `CPF`, `CNPJ`, `PIX`) são permitidos no código, mas devem ser adaptados ao estilo `snake_case` com contexto em inglês (ex: `cpf_validator`, `handle_pix_webhook`).
