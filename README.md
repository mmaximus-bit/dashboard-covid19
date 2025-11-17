# Dashboard COVID-19: Análise de Vacinação vs. Mortalidade

Dashboard interativo para análise da relação entre vacinação e mortalidade durante a pandemia de COVID-19.

## 📊 Funcionalidades

- **KPIs Globais**: Métricas mundiais de casos, mortes e vacinação
- **Filtros Interativos**: Seleção de país/região e período de análise
- **Gráficos Dinâmicos**:
  - Evolução de casos e mortes ao longo do tempo
  - Impacto da vacinação na curva de mortalidade (eixo Y duplo)
- **Análise de Correlação**: Matriz de correlação e interpretação estatística
- **Fonte de Dados**: Our World in Data (OWID) - atualizado automaticamente

## 🛠️ Tecnologias

- **Streamlit**: Interface interativa do dashboard
- **Pandas**: Manipulação e análise de dados
- **Plotly Express**: Visualizações interativas

## 📦 Instalação

1. Clone ou baixe este repositório

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

## 🚀 Como Executar

### Opção 1: Executar o Dashboard Streamlit

```bash
streamlit run dashboard.py
```

O dashboard abrirá automaticamente no seu navegador em `http://localhost:8501`

### Opção 2: Usar o Notebook Jupyter

1. Abra o arquivo `dashboard.ipynb` no Jupyter ou VS Code

2. Execute todas as células para explorar os dados e gerar o arquivo `dashboard.py`

3. A última célula exporta automaticamente o código completo

## 📁 Estrutura do Projeto

```
.
├── dashboard.ipynb      # Notebook Jupyter com análise organizada
├── dashboard.py         # Script Streamlit (gerado pelo notebook)
├── requirements.txt     # Dependências do projeto
└── README.md           # Este arquivo
```

## 📈 Como Usar o Dashboard

1. **Selecione o País/Região**: Use o filtro na barra lateral para escolher entre "Mundo" ou países específicos

2. **Ajuste o Período**: Selecione o intervalo de datas para análise

3. **Explore os Gráficos**: 
   - Visualize a evolução de casos e mortes
   - Analise o impacto da vacinação
   - Examine a correlação estatística entre as variáveis

4. **Interprete os Resultados**: Leia as conclusões baseadas na análise de correlação

## ⚠️ Nota Metodológica

Este dashboard apresenta **correlações estatísticas**, não causalidade. Para análises mais robustas, considere:

- Modelagem de séries temporais com defasagens (time lags)
- Ajuste por população e densidade demográfica
- Estratificação por faixa etária e grupos de risco
- Análise de variantes virais e medidas de contenção

## 📚 Fonte de Dados

**Our World in Data (OWID)**  
https://ourworldindata.org/coronavirus

Os dados são carregados diretamente da fonte e atualizados automaticamente.

## 🤝 Contribuições

Sugestões e melhorias são bem-vindas! Este projeto foi desenvolvido para fins educacionais e de análise exploratória.

## 📄 Licença

Este projeto utiliza dados públicos do OWID. Consulte as diretrizes de uso em:  
https://ourworldindata.org/how-to-use-our-world-in-data

---

**Desenvolvido com ❤️ para análise de dados de saúde pública**
