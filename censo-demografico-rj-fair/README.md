# Desigualdades Socioterritoriais, Estrutura Familiar e Mortalidade no Rio de Janeiro (Censo 2022)

[![FAIR Compliant](https://img.shields.io/badge/FAIR-Compliant-success.svg)](data/data_dictionary.md)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg)](requirements.txt)
[![Data Source: IBGE](https://img.shields.io/badge/Source-IBGE%20Censo%202022-orange.svg)](https://www.ibge.gov.br)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub Pages](https://img.shields.io/badge/Article-GitHub%20Pages-green.svg)](docs/index.html)

**Autores:** Ysis Barbosa Gomes & Ygor Barbosa Gomes  
**Docente / Orientador:** Prof. Alexandre Neves Louzada  
**Curso:** Bacharelado em Sistemas de Informação — 6º Período  
**Disciplina:** Linguagem de Programação (Análise e Visualização de Dados com Python)  
**Natureza:** Projeto Final Teórico-Prático de Conclusão de Disciplina  
**Artigo Acadêmico Publicado:** [Acesse a publicação em docs/index.html](docs/index.html) (ou via GitHub Pages)  

---

## 📌 Resumo Executivo
Este projeto desenvolve uma análise multidimensional sobre os microdados da amostra do Censo Demográfico 2022 para o Estado do Rio de Janeiro (UF 33), disponibilizados pelo IBGE. O estudo investiga as clivagens no saneamento básico entre áreas urbanas e rurais, a vulnerabilidade econômica associada à chefia familiar por raça e gênero, e os padrões de sobremortalidade decorrentes do ápice da crise sanitária de 2021. Todo o projeto é estruturado conforme as diretrizes internacionais da Ciência Aberta e os Princípios FAIR.

**Palavras-chave:** Censo Demográfico 2022; Rio de Janeiro; Análise de Dados; Python; Princípios FAIR; Ciência Aberta.

---

## 🔬 Perguntas de Pesquisa (Research Questions)
- **RQ1:** Quais as disparidades no acesso ao saneamento básico e à conectividade digital entre domicílios urbanos e rurais fluminenses, e de que forma a renda per capita condiciona essa universalização?
- **RQ2:** De que maneira o gênero, raça/cor e arranjo de parentesco da pessoa responsável pela família influenciam o rendimento familiar per capita e a taxa de extrema pobreza?
- **RQ3:** Como se caracterizou a dinâmica de mortalidade domiciliar registrada no Rio de Janeiro entre 2019 e 2022, destacando o choque da COVID-19 em 2021?

---

## 🏛️ Conformidade com os Princípios FAIR
- **Findable (Localizável):** Metadados descritivos completos, catálogo de variáveis em `data/data_dictionary.md`, identificação formal de autoria e links perenes para o repositório FTP do IBGE.
- **Accessible (Acessível):** Repositório de código aberto, rotina de download automatizada em `data/raw/download_raw_data.py` e publicação web interativa responsiva em `docs/index.html`.
- **Interoperable (Interoperável):** Dicionário semântico estruturado e persistência de dados em padrões universais abertos (Apache Parquet e CSV comprimido com GZIP).
- **Reusable (Reutilizável):** Licença aberta MIT, dependências com versões rigorosamente congeladas em `requirements.txt` e pipeline de ETL determinístico executável em comando único.

---

## 📂 Arquitetura do Repositório
```text
censo-demografico-rj-fair/
├── README.md                  # Documentação do projeto, instruções e badges
├── LICENSE                    # Licença de código aberto (MIT)
├── requirements.txt           # Dependências com versões estritas pinadas
├── .gitignore                 # Arquivos temporários e dados brutos volumosos
│
├── data/
│   ├── raw/                   # Scripts de download e instruções dos dados originais
│   │   ├── download_raw_data.py
│   │   └── README.md
│   ├── processed/             # Bases tratadas em Parquet e CSV comprimido
│   │   ├── domicilios_rj_clean.parquet (e .csv.gz)
│   │   ├── familias_rj_clean.parquet (e .csv.gz)
│   │   ├── mortalidade_rj_clean.parquet (e .csv.gz)
│   │   ├── pessoas_amostra_rj_clean.parquet (e .csv.gz)
│   │   └── domicilios_obitos_integrados.parquet
│   └── data_dictionary.md     # Metadados e dicionário de variáveis (FAIR)
│
├── notebooks/
│   └── analise_exploratoria.ipynb  # Exploração preliminar e prototipação
│
├── src/
│   ├── __init__.py
│   ├── etl.py                 # Pipeline de ingestão, limpeza e métricas
│   └── visualizations.py      # Geração de gráficos estáticos e interativos
│
└── docs/                      # Artigo acadêmico estático para GitHub Pages
    ├── index.html             # Publicação científica completa estruturada em HTML5
    └── assets/                # Figuras estáticas de alta resolução e gráficos Plotly
```

---

## 🚀 Como Reproduzir o Projeto Localmente

### 1. Clonagem e Configuração do Ambiente
```bash
git clone https://github.com/ysisbarbosa/censo-demografico-rj-fair.git
cd censo-demografico-rj-fair

# Criar ambiente virtual Python
python -m venv .venv

# Ativar ambiente virtual
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Instalar dependências exatas
pip install -r requirements.txt
```

### 2. Download dos Microdados Oficiais do IBGE
```bash
python data/raw/download_raw_data.py
```

### 3. Execução do Pipeline de Engenharia de Dados (ETL)
```bash
python src/etl.py
```

### 4. Geração dos Gráficos e Visualizações
```bash
python src/visualizations.py
```

### 5. Visualização do Artigo Científico e Notebook
Abra o arquivo `docs/index.html` em seu navegador web para visualizar o artigo com gráficos interativos, ou inicie o Jupyter para explorar o notebook:
```bash
jupyter notebook notebooks/analise_exploratoria.ipynb
```

---

## 📊 Principais Resultados Empíricos
1. **Saneamento e Território (RQ1):** Enquanto 81,6% dos domicílios urbanos contam com esgotamento sanitário adequado, apenas 10,6% dos domicílios rurais têm acesso, demonstrando grave exclusão sanitária fora dos núcleos urbanos.
2. **Interseccionalidade Familiar (RQ2):** Famílias chefiadas por mulheres pretas e pardas têm renda per capita mediana de R$ 750 a R$ 850, em comparação a R$ 1.250 em lares chefiados por homens brancos. Em mães solo com filhos, a extrema pobreza supera 28%.
3. **Mortalidade Domiciliar (RQ3):** Em 2021, os óbitos domiciliares reportados no Rio de Janeiro cresceram 41,8% em relação a 2019 (período basal), refletindo o ápice do excesso de mortes causado pela COVID-19.

---

## 📜 Licença
Este projeto de software é distribuído sob a Licença MIT. Os dados estatísticos são de domínio público, disponibilizados pelo IBGE sob os termos da Lei de Acesso à Informação.
