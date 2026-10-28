# Trading Lab (v0.1)

Projeto educacional para estudar dados históricos e backtesting de estratégias simples para o mercado brasileiro. **Esta versão é exclusivamente simulada**: não conecta a corretoras e não envia ordens.

## Requisitos

- Docker Desktop com Docker Compose, ou Python 3.12+
- CSV de dados históricos cujo uso você tenha autorização para realizar

## Executar com Docker

Na raiz do repositório:

```bash
docker compose up --build
```

O resultado será gravado em `reports/backtest_results.csv`. O CSV de exemplo é **sintético** e serve apenas para validar o funcionamento do código; não representa cotações reais da B3.

Executar os testes:

```bash
docker compose run --rm trading-lab pytest -q
```

## Executar localmente (opcional)

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m pytest -q
python -m trading_lab.main --csv data/sample_prices.csv --output reports/backtest_results.csv
```

Linux/macOS:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m pytest -q
python -m trading_lab.main --csv data/sample_prices.csv --output reports/backtest_results.csv
```

## Formato esperado do CSV

Cabeçalhos obrigatórios: `date,close`. A data deve ser interpretável pelo Pandas e o fechamento deve ser numérico e positivo.

```csv
date,close
2025-01-02,10.00
2025-01-03,10.15
2025-01-06,10.08
```

Para usar dados reais, substitua o arquivo ou passe outro caminho com `--csv`. Verifique a origem, os ajustes por eventos corporativos, a moeda, o fuso horário e os termos de uso do fornecedor.

## O que faz o backtest?

- Calcula médias móveis simples curta e longa.
- Mantém posição comprada quando a média curta está acima da longa; caso contrário, fica fora do mercado.
- Usa o sinal calculado no fechamento de uma barra para simular a execução no fechamento da barra seguinte.
- Deduz um custo percentual configurável sobre o giro da posição.
- Produz retornos e patrimônio acumulado **teóricos**.

O custo padrão de 0,1% por mudança integral de posição é apenas um parâmetro ilustrativo, não uma estimativa de custos reais de uma operação na B3. Configure-o conforme o ativo, corretora, spread, emolumentos, tributos e hipótese de execução.

## Limitações importantes

- Estratégia de demonstração, não recomendação de investimento.
- O modelo não inclui livro de ofertas, fila, liquidez, leilões, limites de preço, execução parcial nem todos os custos de mercado.
- O CSV sintético não permite inferir lucratividade.
- Resultados históricos não garantem resultados futuros.
- Antes de interpretar resultados, use dados reais autorizados, valide a qualidade deles e teste em períodos não usados para desenvolver a estratégia.
- Não conecte este protótipo a uma conta real sem uma revisão de risco, segurança e execução.

## Próximas evoluções

1. Validação mais rigorosa de CSVs e metadados da fonte.
2. Métricas de drawdown, volatilidade e comparação com buy-and-hold.
3. Testes fora da amostra e análise de sensibilidade dos custos.
4. Paper trading com feed de mercado autorizado, mantendo ordens fictícias.
