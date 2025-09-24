# Persistência Poliglota

Este projeto demonstra o conceito de persistência poliglota, utilizando diferentes tipos de bancos de dados para armazenar dados de acordo com suas características e necessidades específicas. A aplicação é construída com Streamlit, oferecendo uma interface interativa para gerenciar cidades e locais, além de funcionalidades de geoprocessamento.




## Tecnologias Utilizadas

*   **Streamlit**: Para a interface de usuário interativa.
*   **SQLite**: Banco de dados relacional para persistência de dados tabulares (cidades e estados).
*   **MongoDB**: Banco de dados de documentos (NoSQL) para persistência de locais e dados geoespaciais.
*   **Geoprocessamento**: Funções para cálculo de distâncias e filtragem por raio, podendo utilizar `geopy` ou consultas geoespaciais nativas do MongoDB.
*   **Python**: Linguagem de programação principal do projeto.




## Fluxo de Dados - Passo a Passo

A aplicação segue um fluxo de dados claro e interativo, conforme detalhado abaixo:

1.  **Inicialização da Aplicação**: O usuário inicia a aplicação Streamlit (`app.py`).
2.  **Cadastro de Cidade**: Através de um formulário na interface, o usuário insere o nome e o estado de uma cidade. A função `inserir_cidade(nome, estado)` é chamada e os dados são salvos no banco de dados SQLite (`dados.db`), com um ID único gerado para a cidade.
3.  **Cadastro de Local**: Um formulário permite ao usuário cadastrar um local, que é salvo como um documento JSON no MongoDB. É recomendado que o `cidade_id` do SQLite seja salvo neste documento para garantir uma ligação confiável entre as cidades e seus locais.
4.  **Consulta por Cidade**: A aplicação (`app.py`) solicita a lista de cidades do SQLite através da função `listar_cidades()`. O usuário seleciona uma cidade, e a aplicação então chama `listar_locais_por_cidade(cidade)` ou filtra por `cidade_id` no MongoDB para exibir uma lista de locais ou um mapa com os locais da cidade selecionada.
5.  **Busca por Proximidade**: A aplicação (`app.py`) obtém uma coordenada de referência e chama a função `geoprocessamento.locais_proximos()` (ou utiliza a consulta `$near` do MongoDB) para encontrar e exibir locais próximos, juntamente com suas distâncias.




## Componentes do Projeto

### `db_mongo.py` - Banco de Documentos (MongoDB) para Locais/GeoJSON

Este módulo é responsável por gerenciar a persistência de locais e dados geoespaciais no MongoDB. Ele armazena documentos JSON com coordenadas e metadados dos locais, permitindo operações de inserção, listagem e consultas por cidade ou proximidade.

**Exemplo de Documento Simples:**
```json
{
    "_id": ObjectId("..."),
    "nome_local": "Praça da Independência",
    "cidade": "João Pessoa",
    "coordenadas": {"latitude": -7.11532, "longitude": -34.861},
    "descricao": "Ponto turístico central"
}
```

**Funções Típicas:**
*   `inserir_local(nome_local, cidade, latitude, longitude, descricao)`: Insere um novo documento de local.
*   `listar_locais()`: Retorna uma lista (cursor) de dicionários Python contendo todos os locais.
*   `listar_locais_por_cidade(cidade)`: Filtra e retorna locais com base no campo `cidade`.




### `db_sqlite.py` - Banco Relacional para Cidades/Estados (Dados Tabulares)

Este módulo é responsável por gerenciar a persistência tabular de cidades e estados utilizando SQLite. Ele mantém uma tabela `cidades` (com `id`, `nome`, `estado`) e oferece funções CRUD básicas.

**Funções Essenciais:**
*   `criar_tabela()`: Cria a tabela `cidades` se ela ainda não existir.
*   `inserir_cidade(nome, estado)`: Insere um novo registro de cidade.
*   `listar_cidades()`: Retorna uma lista de tuplas `(id, nome, estado)` de todas as cidades cadastradas.

**Boas Práticas/Melhorias Sugeridas:**
*   Utilizar `with sqlite3.connect(DB_NAME) as conn:` para garantir `commit`/`close` automáticos.
*   Adicionar `UNIQUE(nome, estado)` para evitar duplicatas.
*   Implementar `get_cidade_por_id(id)` para melhor integração com MongoDB (recomendado usar ID numérico como referência).




### `geoprocessamento.py` - Cálculos de Distância e Filtragem por Raio

Este módulo contém funções para calcular distâncias entre coordenadas geográficas e filtrar locais por proximidade. É fundamental para a funcionalidade de busca por locais próximos na aplicação.

**Funções Comuns:**
*   `calcular_distancia(coord1, coord2) -> float`: Recebe duas coordenadas (latitude, longitude) e retorna a distância em quilômetros. Exemplo: `calcular_distancia((-7.11532, -34.861), (-7.12000, -34.860))` retorna aproximadamente 0.5 km.
*   `locais_proximos(lista_locais, coord_ref, raio_km=10) -> list`: Recebe uma lista de locais do MongoDB (cada um com coordenadas), uma coordenada de referência e um raio em km. Retorna os locais que estão dentro do raio especificado, com a distância calculada. Pode retornar uma lista de dicionários no formato `[{'nome_local': ..., 'distancia_km': ..., 'doc': local }]`.

**Observações:**
*   A biblioteca `geopy` é precisa e simples para cálculos de distância. No entanto, para um grande número de pontos, o cálculo local pode se tornar lento. Nesses casos, o ideal é utilizar consultas geoespaciais nativas do MongoDB para filtrar diretamente no banco de dados, aproveitando seus índices.




### `app.py` - Interface (Streamlit) e "Cola" entre Tudo

O `app.py` é o ponto de entrada da aplicação, responsável por renderizar a interface do usuário (formulários, botões, mapa, resultados). Ele atua como a "cola" que integra todos os módulos do projeto.

**Funcionalidades Principais:**
*   Recebe entradas do usuário (nome da cidade, coordenadas, etc.).
*   Chama as funções apropriadas dos módulos de banco de dados (SQLite e MongoDB) e das funções de geoprocessamento.
*   Exibe os resultados na tela de forma interativa.

**Partes Típicas:**
*   **Imports**: Importa bibliotecas como `streamlit`, `pandas`, `folium` / `streamlit_folium`, e os módulos locais `db_sqlite`, `db_mongo`, `geoprocessamento`.
*   **Inicialização**: Chama `criar_tabela()` do módulo `db_sqlite` para garantir que a tabela de cidades exista.
*   **Sidebar / Menu**: Permite ao usuário navegar entre as opções de "Cadastro Cidade", "Cadastro Local", "Consultar" e "Mapa".
*   **Formulários**: Gerencia a entrada de dados para o cadastro de cidades (chamando `inserir_cidade(nome, estado)`) e locais (chamando `inserir_local(...)`).




### Consultas e Mapas (continuação de `app.py`)

*   **Listagem de Cidades**: Lista as cidades do SQLite (via `listar_cidades`) para preencher um `selectbox` na interface.
*   **Filtragem de Locais**: Filtra locais do MongoDB por cidade (usando a função de listagem apropriada) e exibe os resultados em uma tabela ou marcadores em um mapa.
*   **Proximidade**: Pode chamar `locais_proximos()` do módulo `geoprocessamento` para mostrar locais dentro de um raio específico.

**Observações Importantes sobre `app.py`:**
*   O Streamlit reexecuta todo o `app.py` a cada interação. Para manter estados entre execuções, utilize `st.session_state`.
*   Trate erros com blocos `try/except` e utilize `st.error(...)` para exibir mensagens claras ao usuário.
*   Sempre valide as coordenadas de latitude (entre -90 e 90) e longitude (entre -180 e 180) antes de salvar.




## Repositório do Projeto

Você pode encontrar o código-fonte completo deste projeto no seguinte link:
[https://github.com/Diogo2624/persistencia_poliglota.git](https://github.com/Diogo2624/persistencia_poliglota.git)

## Autores

[Maynard Diogo](https://github.com/Diogo2624)
[Emanuel Messias](https://github.com/manel-mendonca)
Thiago Dionísio



