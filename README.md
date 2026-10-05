# ClearBank: Análise Financeira de Transações

Projeto final do módulo **Análise de Dados e Inteligência de Negócios com IA**. Um notebook Python que lê, valida e limpa um histórico mensal de transações bancárias exportado em CSV, calcula métricas financeiras por mês, sinaliza transações suspeitas e exporta o resultado em JSON.

## O que o projeto faz

1. Lê `transacoes.csv` com o módulo `csv` nativo (sem pandas na solução principal).
2. Valida cada linha (id, cliente, data, tipo e valor) e descarta silenciosamente as inválidas.
3. Agrupa as transações válidas por mês e calcula: quantidade, total de crédito, total de débito, saldo, valor médio, maior e menor valor.
4. Sinaliza como suspeita qualquer transação com valor acima de `R$ 10.000,00`.
5. Exibe um relatório formatado no terminal (saída da célula de execução principal).
6. Salva o resultado da análise em `relatorio.json`.

Requisitos opcionais implementados:

- **Análise com pandas** (`analise_pandas.py`): mesma limpeza e agrupamento mensal feitos com `pandas`, comparados com o resultado da solução nativa dentro do próprio notebook.
- **Visualização com matplotlib** (`grafico.png`): gráfico de barras com o saldo mensal (crédito − débito).

## Como executar

**Google Colab**
1. Faça upload de `desafio-final.ipynb` e `transacoes.csv` (e `analise_pandas.py`, se quiser rodar a seção opcional de pandas) para o mesmo ambiente/pasta.
2. Abra `desafio-final.ipynb` e execute todas as células em ordem (`Ambiente de execução → Executar tudo`).

**Jupyter local**
```bash
pip install pandas matplotlib jupyter
jupyter notebook desafio-final.ipynb
```
Execute as células em ordem, de cima para baixo. Requer Python 3.10+.

## O que o notebook gera como saída

- Relatório mensal e lista de transações suspeitas impressos no terminal.
- `relatorio.json`: relatório completo (período analisado, totais de validação, métricas por mês e transações suspeitas).
- `grafico.png`: gráfico de barras do saldo mensal (requisito opcional).

## Estrutura do repositório

```
clearbank-analise/
├── desafio-final.ipynb   # notebook principal, com saídas salvas
├── analise_pandas.py      # análise alternativa com pandas (opcional)
├── transacoes.csv         # dados de entrada (20 transações válidas, 5 inválidas, 4 meses)
├── relatorio.json          # saída gerada pelo notebook
├── grafico.png             # gráfico gerado pelo notebook (opcional)
└── README.md
```
