# Exercício Prático 3: Fecho Convexo - INF2604

Este projeto implementa e analisa o algoritmo Gift Wrapping para calcular o fecho convexo de conjuntos de pontos com diferentes tamanhos.

## Configuração

1. Criar e ativar um ambiente virtual:
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1 
```

2. Instalar dependências:
```bash
pip install -r requirements.txt
```

## Uso

Execute o script principal:
```bash
python fecho_convexo.py
```

Isso irá:
- Processar 19 tamanhos diferentes de nuvens de pontos (de 4 a 1.048.576 pontos)
- Executar 1.000 vezes cada tamanho para análise estatística
- Calcular o fecho convexo usando o algoritmo Gift Wrapping
- Gerar gráficos de visualização para cada tamanho
- Criar análise de complexidade computacional
- Salvar todos os dados em arquivos CSV e PNG

## Resultados

O programa gera:
- **Gráficos individuais**: `fecho_convexo_2eXX.png` para cada tamanho
- **Dados do fecho**: `fecho_convexo_2eXX.csv` com pontos do fecho convexo para cada tamanho
- **Dados de tempo**: `tempos_execucao.csv` com 19.000 execuções
- **Análise de complexidade**: `analise_complexidade.png`

## Dependências

- matplotlib >= 3.5.0
- numpy >= 1.20.0
- scipy >= 1.7.0
