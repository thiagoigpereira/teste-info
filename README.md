# Sistema de Automação de Relatórios de Campanhas

Aplicação local em Python para importar, normalizar, consolidar e exportar planilhas de campanhas de marketing. A primeira versão foi desenhada para aceitar arquivos CSV e XLSX, incluindo exportações do Sprout Social e planilhas preenchidas manualmente, sem depender de formatos fixos de coluna.

## Funcionalidades

- Importa todos os arquivos `.csv` e `.xlsx` encontrados em pastas configuradas.
- Lê todas as abas de arquivos Excel e preserva o nome da aba em `source_sheet`.
- Incorpora automaticamente campanhas manuais de `data/manual/`.
- Normaliza colunas por meio de aliases definidos em JSON.
- Consolida os dados em uma base canônica única.
- Preserva metadados de auditoria: `source_file`, `source_type`, `source_sheet` e `imported_at`.
- Registra arquivos processados, erros de importação, colunas desconhecidas, colunas ausentes e quantidade de registros.
- Exporta `consolidated.csv` e `consolidated.xlsx` em `data/output/`.
- Expõe CLI com comandos separados para cada etapa do pipeline.

## Estrutura

```text
.
├── config/
│   └── column_mapping.json
├── data/
│   ├── input/
│   ├── manual/
│   ├── processed/
│   └── output/
├── src/
│   ├── cli/
│   ├── config/
│   ├── exporters/
│   ├── importers/
│   ├── services/
│   └── transformers/
├── tests/
├── .env
├── main.py
├── requirements.txt
└── README.md
```

## Requisitos

- Python 3.12+
- Dependências listadas em `requirements.txt`:
  - pandas
  - openpyxl
  - pydantic
  - typer
  - python-dotenv

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Configuração

As pastas e o arquivo de mapeamento são configurados em `.env`:

```env
CAMPAIGN_INPUT_DIR=data/input
CAMPAIGN_MANUAL_DIR=data/manual
CAMPAIGN_PROCESSED_DIR=data/processed
CAMPAIGN_OUTPUT_DIR=data/output
CAMPAIGN_COLUMN_MAPPING=config/column_mapping.json
```

O arquivo `config/column_mapping.json` define o padrão interno e os nomes alternativos aceitos para cada coluna:

```json
{
  "alcance": ["reach", "alcance"],
  "impressoes": ["impressions", "impressoes"],
  "engajamento": ["engagement", "engajamento"]
}
```

A aplicação também considera o próprio nome canônico como alias. A comparação ignora maiúsculas/minúsculas, espaços, hífens e acentos.

## Como usar

Coloque arquivos de campanhas automáticas em:

```text
data/input/
```

Coloque planilhas manuais em:

```text
data/manual/
```

Execute os comandos pela CLI:

```bash
python main.py import
python main.py consolidate
python main.py export
python main.py run-all
```

### O que cada comando faz

- `python main.py import`: lê arquivos de `data/input/` e `data/manual/` e gera `data/processed/imported_raw.csv`.
- `python main.py consolidate`: aplica o mapeamento de colunas e gera `data/processed/consolidated.csv`.
- `python main.py export`: exporta `data/output/consolidated.csv` e `data/output/consolidated.xlsx`.
- `python main.py run-all`: executa importação, consolidação e exportação em sequência.

## Exemplos

Entradas de exemplo foram incluídas em:

- `data/input/sprout_social_example.csv`
- `data/manual/manual_campaign_example.csv`

Saída consolidada ilustrativa:

- `data/output/consolidated_example.csv`

Para gerar a saída real com os exemplos, execute:

```bash
python main.py run-all
```

## Logs

Os logs são gravados em:

```text
data/processed/campaign_automation.log
```

Eles incluem:

- arquivos processados;
- erros de leitura;
- colunas não reconhecidas;
- colunas canônicas ausentes adicionadas como vazias;
- quantidade de registros importados e consolidados.

## Testes

Os testes usam `unittest` da biblioteca padrão:

```bash
python -m unittest discover -s tests
```

## Extensão para novos formatos

Para adicionar novos formatos no futuro:

1. Crie uma classe que herde de `DataImporter` em `src/importers/`.
2. Defina as extensões suportadas.
3. Implemente o método `read` retornando um `pandas.DataFrame`.
4. Registre o novo importador em `ImporterFactory`.

Essa separação mantém a importação desacoplada da transformação e da exportação.
